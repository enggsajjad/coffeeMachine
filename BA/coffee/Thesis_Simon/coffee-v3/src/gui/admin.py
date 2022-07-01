import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from gui.admin_gen import Ui_Dialog
from gui.journal_widget import JournalWidget


class Admin(QDialog, Ui_Dialog):
    exit_app = pyqtSignal()
    set_maintenance = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.unlocked = False

        self.journal = JournalWidget(self)
        self.journal.setGeometry(0, 160, self.width(), self.height() - 160)

        self.maintenance.toggled.connect(self.set_maintenance.emit)
        self.restart.clicked.connect(self.exit_app.emit)

    def reset(self):
        self.maintenance.setChecked(False)
