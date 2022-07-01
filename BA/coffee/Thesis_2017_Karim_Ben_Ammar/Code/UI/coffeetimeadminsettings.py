import sys

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal

import coffeeTimeAdminSettings_auto

class CoffeeTimeAdminSettings(QDialog, coffeeTimeAdminSettings_auto.Ui_Dialog):

 returnAdmin = pyqtSignal()

 def backToAdmin(self):
  self.returnAdmin.emit()

 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)
  self.backButton.clicked.connect(lambda : self.backToAdmin())
