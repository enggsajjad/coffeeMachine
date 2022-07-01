import datetime
import multiprocessing
import os
import sys
import time

from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from gui.unregistered_uid_gen import Ui_Dialog

class UnregisteredUid(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


    @pyqtSlot(str)
    def display_uid(self, uid):
        print(uid)
        self.uid.setText(uid)
