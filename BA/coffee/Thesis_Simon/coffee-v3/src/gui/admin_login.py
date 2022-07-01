from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

from gui.admin_login_gen import Ui_Dialog


class AdminLogin(QDialog, Ui_Dialog):
    login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.password = "7890"
        self.tempPassword = ""

        self.zero.clicked.connect(lambda: self.checkPassword("0"))
        self.one.clicked.connect(lambda: self.checkPassword("1"))
        self.two.clicked.connect(lambda: self.checkPassword("2"))
        self.three.clicked.connect(lambda: self.checkPassword("3"))
        self.four.clicked.connect(lambda: self.checkPassword("4"))
        self.five.clicked.connect(lambda: self.checkPassword("5"))
        self.six.clicked.connect(lambda: self.checkPassword("6"))
        self.seven.clicked.connect(lambda: self.checkPassword("7"))
        self.eight.clicked.connect(lambda: self.checkPassword("8"))
        self.nine.clicked.connect(lambda: self.checkPassword("9"))

        self.back.clicked.connect(self.clearPassword)
        self.clear.clicked.connect(self.clearPassword)
        self.enter.clicked.connect(self.enterPassword)

    def checkPassword(self, num):
        self.tempPassword += num

    def clearPassword(self):
        self.tempPassword = ""

    def enterPassword(self):
        if self.tempPassword == self.password:
            self.login.emit()
            self.tempPassword = ""
