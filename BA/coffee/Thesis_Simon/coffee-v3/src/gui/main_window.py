import atexit
import datetime
import os
import sys
import logging

from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

from gui.main_window_gen import Ui_MainWindow

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_MainWindow):
    # signals going IN; emitted by importing module
    get_uid = pyqtSignal()
    got_user = pyqtSignal(str, int, bool, str, int)
    got_order = pyqtSignal(bool, bool)
    unregistered_user = pyqtSignal(str)
    water_alert_changed = pyqtSignal(bool)
    wait_order_complete = pyqtSignal()
    is_rinsing = pyqtSignal()
    exit_app = pyqtSignal()

    # signals going OUT; emitted by gui
    order_complete = pyqtSignal(bool, bool)
    set_maintenance = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        QIcon.setThemeName("PiXflat")

        # Connect get_uid_widget in gui
        self.get_uid_widget.admin_button.clicked.connect(lambda:
            self.stackedWidget.setCurrentWidget(self.admin_login_widget))

        # Connect got_user_widget in gui
        self.order_complete = self.got_user_widget.order_complete
        self.order_complete.connect(lambda: self.get_uid_widget.show_making_coffee(True))
        self.order_complete.connect(lambda: self.stackedWidget.setCurrentWidget(self.get_uid_widget))

        # Connect admin_login_widget in gui
        self.admin_login_widget.back.clicked.connect(self.reset)
        self.admin_login_widget.login.connect(lambda:
            self.stackedWidget.setCurrentWidget(self.admin_widget))

        # Connect admin_widget in gui
        self.set_maintenance = self.admin_widget.set_maintenance
        self.admin_widget.exit_app.connect(self.exit_app.emit)
        self.admin_widget.back.clicked.connect(self.reset)

        # Connect water_alert_widget in gui
        self.water_alert_changed.connect(self.handle_water_alert)

        # Connect unregistered_uid_widget in gui
        self.unregistered_user.connect(self.unregistered_uid_widget.display_uid)
        self.unregistered_user.connect(lambda:
            self.stackedWidget.setCurrentWidget(self.unregistered_uid_widget))
        self.unregistered_uid_widget.button.clicked.connect(self.reset)

        # Connect widgets with interfacing IN/OUT signals
        self.cancel = self.got_user_widget.cancel
        self.cancel.connect(self.reset)

        self.get_uid.connect(lambda: self.get_uid_widget.show_making_coffee(False))
        self.get_uid.connect(lambda: self.stackedWidget.setCurrentWidget(self.get_uid_widget))

        self.got_user.connect(self.got_user_widget.display_user)
        self.got_user.connect(lambda: self.stackedWidget.setCurrentWidget(self.got_user_widget))
        self.got_order.connect(self.got_user_widget.display_order)
        self.wait_order_complete.connect(self.got_user_widget.start_ok_timer)

        self.reset()

    def reset(self):
        self.stackedWidget.setCurrentWidget(self.get_uid_widget)
        self.admin_widget.reset()

    @pyqtSlot(bool)
    def handle_water_alert(self, has_water):
        if has_water:
            self.reset()
        else:
            self.stackedWidget.setCurrentWidget(self.water_alert_widget)
