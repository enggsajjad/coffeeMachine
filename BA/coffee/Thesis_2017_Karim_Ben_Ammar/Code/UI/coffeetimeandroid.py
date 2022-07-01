import sys
import os

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
import coffeeTimeAndroid_auto


class CoffeeTimeAndroid(QDialog, coffeeTimeAndroid_auto.Ui_Dialog):

 def showQr(self):
  self.qrWidget.show()
 def hideQr(self):
  self.qrWidget.hide()
 def showAdd(self):
  self.addWidget.show()
 def hideAdd(self):
  self.addWidget.hide()
 def updatePicture(self):
    if os.path.isfile('/home/pi/CoffeeMachine/UI/userUID.png') and self.repeat :
         self.userQr.setIcon(QIcon('/home/pi/CoffeeMachine/UI/userUID.png'))
         self.repeat = False
    elif not os.path.isfile('/home/pi/CoffeeMachine/UI/userUID.png') and not self.repeat :
         self.userQr.setIcon(QIcon('/home/pi/CoffeeMachine/res/addUserWaiting.png'))
         self.repeat = True

 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)

  self.repeat = True

  self.qrWidget.hide()
  self.addWidget.hide()
  self.downloadButton.clicked.connect(lambda : self.showQr())
  self.qrHide.clicked.connect(lambda : self.hideQr())
  self.registerButton.clicked.connect(lambda : self.showAdd())
  self.addHide.clicked.connect(lambda : self.hideAdd())

  timer = QTimer(self)
  timer.timeout.connect(self.updatePicture)
  timer.start(1000)
