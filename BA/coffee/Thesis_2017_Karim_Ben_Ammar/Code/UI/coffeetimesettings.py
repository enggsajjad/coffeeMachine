import sys
 
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal
import coffeeTimeSettings_auto

class CoffeeTimeSettings(QDialog, coffeeTimeSettings_auto.Ui_Dialog):

 asignal = pyqtSignal()

 def backToOrder(self):
  self.asignal.emit()

 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)
  self.backButton.clicked.connect(lambda : self.backToOrder())
