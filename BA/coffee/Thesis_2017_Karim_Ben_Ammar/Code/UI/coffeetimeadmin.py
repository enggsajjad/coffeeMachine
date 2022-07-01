import sys
import os
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal

import coffeeTimeAdmin_auto

class CoffeeTimeAdmin(QDialog, coffeeTimeAdmin_auto.Ui_Dialog):

 asignal = pyqtSignal()
 logSettings = pyqtSignal()

 def exitApp(self):
  self.asignal.emit()

 def openSettings(self):
  self.logSettings.emit()
 def unlock(self):
  if not self.unlocked:
      with open('/home/pi/CoffeeMachine/UI/unlock.txt', 'a+') as f :
          pass
      with open('/home/pi/CoffeeMachine/UI/maintenance.txt', 'a') as f:
          pass
      self.cleaningMode.setIcon(QIcon("../res/cleaningSelected.png"))
      self.unlocked = True
  else :
      os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")
      os.remove("/home/pi/CoffeeMachine/UI/maintenance.txt")
      self.cleaningMode.setIcon(QIcon("/home/pi/CoffeeMachine/res/cleaningNotSelected.png"))
      self.unlocked = False

 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)
  self.unlocked = False
  self.cleaningMode.clicked.connect(lambda : self.unlock())
  self.exitFullscreen.clicked.connect(lambda : self.exitApp())
