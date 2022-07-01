import atexit
import datetime
import logging
import os
import sys
import time
from logging.handlers import SysLogHandler
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from multiprocessing.connection import wait as poll_all
from threading import Thread

from PyQt5.QtWidgets import QApplication
from transitions import Machine, MachineError

import buzzer
import download_images
import gpio_handler
import gui.main_window as main_window
import order
import rfid_input
import scheduler_thread
import user
from util import DispensingStatus, Msg

# standby is set by "Timer" in the coffeemachine's menu, currently after 3hrs
SLEEP_TIME = 3 * 60 * 60

# show warning when balance below
DISPENSING_WARN = 0

# deny dispensing when balance below
DISPENSING_DENY = -2000  # -20€

class CoffeeMachine():
    states = ['water_alert', 'coffee_ground', 'get_uid', 'unlocked',
              'wait_water_finished', 'wait_coffee_finished', 'wait_order_complete', 'maintenance']

    transitions = [
        # trigger, source, destination
        {'trigger': 'water_level_high', 'source': ['maintenance', 'get_uid'], 'dest': 'water_alert'},
        {'trigger': 'unlock', 'source': 'get_uid', 'dest': 'unlocked'},
        {'trigger': 'water_level_low', 'source': 'water_alert', 'dest': 'get_uid'},
        {'trigger': 'grinder_low', 'source': 'unlocked', 'dest': 'coffee_ground'},
        {'trigger': 'flow_2_started', 'source': 'unlocked',
            'dest': 'wait_water_finished'},
        {'trigger': 'flow_2_stopped', 'source': 'wait_water_finished',
            'dest': 'wait_order_complete'},
        {'trigger': 'flow_1_started', 'source': 'coffee_ground',
            'dest': 'wait_coffee_finished'},
        {'trigger': 'flow_1_stopped', 'source': 'wait_coffee_finished',
            'dest': 'wait_order_complete'},
        {'trigger': 'sleep_detected',
            'source': 'wait_water_finished', 'dest': 'unlocked'},
        {'trigger': 'order_complete',
            'source': 'wait_order_complete', 'dest': 'get_uid'},
        {'trigger': 'maintenance', 'source': '*', 'dest': 'maintenance'},
        {'trigger': 'reset', 'source': ['maintenance', 'unlocked'], 'dest': 'get_uid'},
        # cheating detection
        {'trigger': 'grinder_low', 'source': 'get_uid', 'dest': 'coffee_ground', 'before': 'detect_cheating',
            'conditions': 'cheating_condition'},
        {'trigger': 'flow_2_started', 'source': 'get_uid', 'dest': 'wait_water_finished', 'before': 'detect_cheating',
            'conditions': 'cheating_condition'},
    ]

    connections = {}

    current_user = None
    current_user_ctime = 0
    order_complete_signaled = False
    # if sleep was detected in current session
    sleep_detected_flag = False
    water_alert_flag = False

    # used for order_complete
    coffee = False
    milk = False
    cheated = False

    def __init__(self, rfid_input_conn, gpio_handler_conn, buzzer_conn, main_window):

        self.machine = Machine(self, states=self.states,
                               transitions=self.transitions, queued=True, initial='get_uid')

        self.connections['rfid_input'] = rfid_input_conn
        self.connections['gpio_handler'] = gpio_handler_conn
        self.connections['buzzer'] = buzzer_conn

        self.main_window = main_window
        self.main_window.cancel.connect(self.reset)
        self.main_window.order_complete.connect(self.signal_order_complete)
        self.main_window.set_maintenance.connect(self.set_maintenance)

    def set_maintenance(self, enabled):
        if enabled:
            self.maintenance()
        else:
            self.reset()

    def on_enter_water_alert(self):
        self.main_window.water_alert_changed.emit(False)

    def on_exit_water_alert(self):
        self.main_window.water_alert_changed.emit(True)

    def on_enter_unlocked(self):
        self.connections['rfid_input'].send(Msg.CMD_PAUSE)
        self.connections['gpio_handler'].send(Msg.CMD_UNLOCK)
        self.connections['buzzer'].send(Msg.CMD_UNLOCK)

    def on_exit_unlocked(self):
        self.connections['gpio_handler'].send(Msg.CMD_LOCK)

    def on_enter_get_uid(self):
        self._check_water_alert()

        self.main_window.get_uid.emit()

        self.connections['rfid_input'].send(Msg.CMD_RESUME)
        self.connections['gpio_handler'].send(Msg.CMD_LOCK)
        self.connections['buzzer'].send(Msg.CMD_LOCK)
    
    def on_exit_get_uid(self):
        self.connections['rfid_input'].send(Msg.CMD_PAUSE)

    def on_enter_maintenance(self):
        self.connections['gpio_handler'].send(Msg.CMD_UNLOCK)

    def on_exit_maintenance(self):
        self.connections['gpio_handler'].send(Msg.CMD_LOCK)

    def on_enter_coffee_ground(self):
        self.main_window.got_order.emit(
            # deprecated: value for coffee_milk_pref won't be used
            True, self.current_user.coffee_milk_pref)

    def on_enter_wait_water_finished(self):
        if not self.detect_sleep():
            # note that currently as a workaround for the coffee grinder signal not being recognized sometimes,
            # it might happen that this order still changes to coffee == True. See display_order() in gui/got_user.py for details.
            self.main_window.got_order.emit(
                # only use coffee preference/ ignore water_milk_pref
                False, False)
        else:
            self.main_window.is_rinsing.emit()
            self.sleep_detected()

    def on_enter_wait_order_complete(self):
        # user could complete order (press ok in gui and accept selection) while coffee or water are still being dispensed
        # therefore check if completion was signaled before
        if self.order_complete_signaled:
            self.complete_order()
        else:
            self.main_window.wait_order_complete.emit()

    def on_exit_wait_order_complete(self):
        self.order_complete_signaled = False

    def signal_order_complete(self, coffee, milk):
        self.order_complete_signaled = True
        self.coffee = coffee
        self.milk = milk

        # if coffee/water are finished
        if self.is_wait_order_complete():
            self.complete_order()

    def complete_order(self):
        order.process_order(self.current_user.uid, self.coffee, self.milk, self.cheated)
        self.cheated = False
        self.sleep_detected_flag = False
        # only use coffee preference/ ignore water_milk_pref
        if self.coffee:
            user.update_milk_pref(self.current_user.token, True, self.milk)
        self.order_complete()

    def _handle_flow_started(self, **kwargs):
        if self.is_coffee_ground():
            self.flow_1_started()
        else:
            self.flow_2_started()

    def _handle_flow_stopped(self, **kwargs):
        if self.is_wait_coffee_finished():
            self.flow_1_stopped()
        else:
            self.flow_2_stopped()

    def _handle_water_level_high(self, **kwargs):
        if not self.water_alert_flag:
            self.water_alert_flag = True
            self.water_level_high()

    def _handle_water_level_low(self, **kwargs):
        self.water_alert_flag = False
        self.water_level_low()
    
    def _check_water_alert(self):
        """ check if water alert was raised while doing something else (e.g. making coffee) """
        if self.water_alert_flag:
            self.water_level_high()

    def _handle_grinder_low(self, **kwargs):
        self.grinder_low()

    def _handle_got_id(self, **kwargs):
        conn = kwargs['conn']
        assert type(conn) is Connection, "conn is not a Connection"

        if conn.poll(2):
            uid = conn.recv()

            if not self.is_get_uid():
                LOG.warning("Received uid while not in get_uid state")
                return

            self.current_user = user.get_user(uid)
            self.current_user_ctime = time.time()
            if self.current_user:
                if self.current_user.balance > DISPENSING_DENY:
                    self.unlock()
                    if self.current_user.balance > DISPENSING_WARN:
                        dispensing_status = DispensingStatus.ALLOW
                    else:
                        dispensing_status = DispensingStatus.WARN
                else:
                    LOG.info("Dispensing denied to: %s", self.current_user)
                    dispensing_status = DispensingStatus.DENY

                self.main_window.got_user.emit(
                    self.current_user.name,
                    self.current_user.balance,
                    self.current_user.coffee_milk_pref,
                    order.get_last_order_summary(uid),
                    dispensing_status)

                # testing
                # time.sleep(3)
                # self._handle_flow_started()
                # time.sleep(8)
                # self._handle_flow_stopped()
            else:
                self.main_window.unregistered_user.emit(uid)
                LOG.info("Unregistered user with uid: %s", uid)
        else:
            raise Exception("Expected to receive uid")

    def detect_sleep(self):
        if self.sleep_detected_flag:
            return False
        last_order_dt = order.get_last_order_timestamp()
        if last_order_dt is not None:
            delta = datetime.datetime.utcnow() - last_order_dt
            if delta.total_seconds() > SLEEP_TIME:
                LOG.info("Detected sleep. Last order was %s ago.", delta)
                self.sleep_detected_flag = True
                return True
        return False

    def detect_cheating(self):
        LOG.warning("Cheating detected: %s", self.current_user)
        self.cheated = True
        self.main_window.got_user.emit(
            self.current_user.name,
            self.current_user.balance,
            self.current_user.coffee_milk_pref,
            order.get_last_order_summary(self.current_user.uid),
            DispensingStatus.ALLOW)
    
    def cheating_condition(self):
        return self.current_user is not None and time.time() - self.current_user_ctime < 270 # should be larger than cancel timout

    def handle_connections(self):
        dispatch = {
            Msg.E_FLOW_1_STARTED: self._handle_flow_started,
            Msg.E_FLOW_2_STARTED: self._handle_flow_started,
            Msg.E_FLOW_1_STOPPED: self._handle_flow_stopped,
            Msg.E_FLOW_2_STOPPED: self._handle_flow_stopped,
            Msg.E_WATER_LEVEL_HIGH: self._handle_water_level_high,
            Msg.E_WATER_LEVEL_LOW: self._handle_water_level_low,
            Msg.E_GRINDER_LOW: self._handle_grinder_low,
            Msg.E_GOT_ID: self._handle_got_id,
        }

        while True:
            ready_conns = poll_all(self.connections.values())
            for conn in ready_conns:
                msg = conn.recv()
                try:
                    LOG.debug("Received message: %s", Msg(msg).name)
                    if msg in dispatch:
                        dispatch[msg](conn=conn)
                    # dispatch.get(msg, lambda x: "Not implemented")(conn=conn)
                except ValueError as ve:
                    LOG.exception("Received invalid message")
                except MachineError as me:
                    LOG.error(me.value)


if __name__ == "__main__":
    # Configure logging
    FORMAT_NOTIME = '%(levelname)s [%(name)s] %(message)s'
    FORMAT_TIME = '%(asctime)s '
    if len(sys.argv) > 1 and sys.argv[1] == "--nologtime":
        log_format = FORMAT_NOTIME 
    else:
        log_format = FORMAT_TIME + FORMAT_NOTIME
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    logging.getLogger('transitions').setLevel(logging.INFO)
    logging.getLogger('rfid_input').setLevel(logging.INFO)
    logging.getLogger('pymysql').setLevel(logging.ERROR)
    logging.getLogger('gpio_handler').setLevel(logging.INFO)

    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)

    # setup qt
    app = QApplication(sys.argv)
    form = main_window.MainWindow()
    form.exit_app.connect(sys.exit)
    form.showFullScreen()

    # setup sub processes/threads
    rfid_input_parent_conn, rfid_input_child_conn = Pipe()
    rfid_p = Process(target=rfid_input.read, args=(rfid_input_child_conn,))
    rfid_p.daemon = True

    gpio_handler_parent_conn, gpio_handler_child_conn = Pipe()
    gpio_p = Process(target=gpio_handler.run, args=(gpio_handler_child_conn,))
    gpio_p.daemon = True

    buzzer_parent_conn, buzzer_child_conn = Pipe()
    buzzer_p = Process(target=buzzer.run, args=(buzzer_child_conn,))
    buzzer_p.daemon = True

    cm = CoffeeMachine(rfid_input_parent_conn,
                       gpio_handler_parent_conn, buzzer_parent_conn, form)
    cm_thread = Thread(target=cm.handle_connections)
    cm_thread.daemon = True

    scheduler = scheduler_thread.SchedulerThread()
    scheduler.set_condition(cm.is_get_uid)
    scheduler.add_task(order.push_all)
    scheduler.add_task(download_images.run)
    scheduler.add_task(form.get_uid_widget.reload_images)

    cm_thread.start()
    buzzer_p.start()
    rfid_p.start()
    gpio_p.start()
    LOG.debug("buzzer_pid: %i, rfid_pid: %i, gpio_pid: %i", buzzer_p.pid, rfid_p.pid, gpio_p.pid)
    scheduler.start()

    atexit.register(app.exit)
    sys.exit(app.exec_())
