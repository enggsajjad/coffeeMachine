import logging
import queue
import atexit
import time
import threading

import pigpio

from util import Msg, receive_cmd

LOG = logging.getLogger(__name__)

LOCKPIN = 26 
WATERLEVELPIN = 19 
WATERFLOW1PIN = 5
WATERFLOW2PIN = 6
GRINDERPIN = 13 
PINDESCRIPTION = "[water_level, water_flow1, water_flow2, grinder]"
PINDESCRIPTION_LINES = 20

"""Reads gpio input and passes it on to parent proccess using a pipe"""
class GPIOHandler():
    last_log = ''
    print_log_line_count = 0

    timer_flow1 = None
    timestamp_flow1 = time.time()
    timestamp_flow2 = time.time()

    msg_q = queue.Queue()

    _lock = True

    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(LOCKPIN, pigpio.OUTPUT)

        self.pi.set_mode(WATERLEVELPIN, pigpio.INPUT)
        self.pi.set_mode(WATERFLOW1PIN, pigpio.INPUT)
        self.pi.set_mode(WATERFLOW2PIN, pigpio.INPUT)
        self.pi.set_mode(GRINDERPIN, pigpio.INPUT)
        
        self.pi.set_pull_up_down(WATERLEVELPIN, pigpio.PUD_UP)
        self.pi.set_pull_up_down(WATERFLOW1PIN, pigpio.PUD_UP)
        self.pi.set_pull_up_down(WATERFLOW2PIN, pigpio.PUD_UP)
        self.pi.set_pull_up_down(GRINDERPIN, pigpio.PUD_UP)

        self.current_water_level = self.pi.read(WATERLEVELPIN)
        self.current_water_flow1 = self.pi.read(WATERFLOW1PIN)
        self.current_water_flow2 = self.pi.read(WATERFLOW2PIN)
        self.current_grinder = self.pi.read(GRINDERPIN)

        self.water_flow_started = False

        # only trigger when signal steady for x macroseconds
        # try to filter out random signals, that are triggered when water isn't actually flowing 
        self.pi.set_glitch_filter(WATERFLOW1PIN, 3500) # µs

        self.pi.set_glitch_filter(WATERLEVELPIN, 10000) # µs

        # see gpio_signal_analysis/grinder_deltas_unfiltered.csv
        self.pi.set_glitch_filter(GRINDERPIN, 500000) # µs

        # water_leveldt = MeasureDeltas("water_level")
        # waterdt = MeasureDeltas("water_flow")
        # grinderdt = MeasureDeltas("grinder")
        # self.pi.callback(WATERFLOW1PIN, pigpio.EITHER_EDGE, waterdt.deltas)
        # self.pi.callback(WATERLEVELPIN, pigpio.EITHER_EDGE, water_leveldt.deltas)
        # self.pi.callback(GRINDERPIN, pigpio.EITHER_EDGE, grinderdt.deltas)

        self.pi.callback(GRINDERPIN, pigpio.FALLING_EDGE, self.detect_grinder)
        self.pi.callback(WATERFLOW1PIN, pigpio.RISING_EDGE, self.detect_water_flow1)
        # self.pi.callback(WATERFLOW2PIN, pigpio.EITHER_EDGE, self.detect_water_flow2)
        self.pi.callback(WATERLEVELPIN, pigpio.EITHER_EDGE, self.detect_water_level)

        # Handle case if started while water level low
        if self.current_water_level == 1:
            self.detect_water_level(0, self.current_water_level, 0)

    def detect_water_flow1(self, _channel, level, _tick):
        self._print_log()
        self.current_water_flow1 = level
        # LOG.debug("detect_water_flow")
        # signal not receiveid continously -> safety delta of 1s
        if time.time() - self.timestamp_flow1 < 10:
            if not self.water_flow_started:
                LOG.debug("detect_water_flow1: detected and started")
                self.msg_q.put(Msg.E_FLOW_1_STARTED)
                self.water_flow_started = True
                self.timer_flow1 = ResetableTimer(10000, self.water_flow1_stopped)
                self.timer_flow1.start()
                # LOG.debug("detect_water_flow1: timer started")
            
            self.timer_flow1.reset()
            LOG.debug("detect_water_flow1: detected and timer reset")
        else:
            LOG.debug("detect_water_flow1: delta since last trigger passed")


        self.timestamp_flow1 = time.time()

    def water_flow1_stopped(self):
        if self.water_flow_started:
            LOG.debug("water_flow1_stopped")
            self.msg_q.put(Msg.E_FLOW_1_STOPPED)
            self.water_flow_started = False

    def detect_water_flow2(self, _channel, level, _tick):
        self.current_water_flow2 = level
        # currently flow1 and flow2 signal are the same, hardware bug

    def detect_grinder(self, _channel, level, _tick):
        self.current_grinder = level
        self._print_log()
        if self.current_grinder == 0:
            LOG.debug("detected grinder low")
            self.msg_q.put(Msg.E_GRINDER_LOW)

    def detect_water_level(self, _channel, level, _tick):
        self.current_water_level = level
        self._print_log()
        if self.current_water_level == 1:
            LOG.debug("Detected water level high")
            self.msg_q.put(Msg.E_WATER_LEVEL_HIGH)
        else:
            LOG.debug("Detected water level low")
            self.msg_q.put(Msg.E_WATER_LEVEL_LOW)

    def lock(self):
        self._lock = True
        self.pi.write(LOCKPIN, 0)

    def unlock(self):
        self._lock = False
        self.pi.write(LOCKPIN, 1)
    
    def rewrite_lock(self):
        # pin output seems to be unstable
        if self._lock:
            self.pi.write(LOCKPIN, 1)
            time.sleep(0.1)
            self.pi.write(LOCKPIN, 0)
        else:
            self.pi.write(LOCKPIN, 0)
            time.sleep(0.1)
            self.pi.write(LOCKPIN, 1)

    def _print_log(self):
        if self.print_log_line_count < PINDESCRIPTION_LINES:
            self.print_log_line_count += 1
        else:
            self.print_log_line_count = 0
            LOG.debug(PINDESCRIPTION)

        LOG.debug("read gpio input: [%i, %i, %i, %i]",
               self.current_water_level, self.current_water_flow1, self.current_water_flow2, self.current_grinder)

def run(conn):
    """Setup gpio inputs and send read values through conn in fixed intervals"""
    gpio_handler = GPIOHandler()
    bind = {
        Msg.CMD_LOCK: gpio_handler.lock,
        Msg.CMD_UNLOCK: gpio_handler.unlock
    }

    LOG.debug("gpio_handler started.")

    while True:
        receive_cmd(conn, bind=bind)

        # write to connection pipe has to be synchronized, therefore buffer msgs in queue
        while gpio_handler.msg_q.qsize() > 0:
            conn.send(gpio_handler.msg_q.get())

        gpio_handler.rewrite_lock()

        time.sleep(0.5)


class ResetableTimer(threading.Thread):

    def __init__(self, millis, callback):
        super().__init__()
        self.millis = millis
        self.callback = callback

        self.timer = millis

        self.reset_event = threading.Event()
        self.cancel_event = threading.Event()

    def run(self):
        while self.timer > 0:
            if self.cancel_event.is_set():
                return
            self.reset_event.wait(0.001)
            self.timer -= 1
            if self.reset_event.is_set():
                self.timer = self.millis
                self.reset_event.clear()


        self.callback()

    def reset(self):
        self.reset_event.set()

    def cancel(self):
        self.cancel_event.set()

class MeasureDeltas():
    deltas_tick = 0

    def __init__(self, name):
        self.name = name
        self.file = open("{}_deltas.csv".format(name), 'a+', buffering=1)
        atexit.register(self.file.close)

    def deltas(self, _channel, level, tick):
        # LOG.debug("name: %s, level: %s, delta: %s", self.name, level, (tick - self.deltas_tick) / 1000)
        self.file.write("{},{},{}\n".format(time.asctime(), tick, level))

        # self.deltas_tick = tick