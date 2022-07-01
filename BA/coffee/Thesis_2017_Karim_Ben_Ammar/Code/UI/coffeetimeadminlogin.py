import sys

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal
import coffeeTimeAdminLogin_auto

class CoffeeTimeAdminLogin(QDialog, coffeeTimeAdminLogin_auto.Ui_Dialog):

 asignal = pyqtSignal()
 backH = pyqtSignal()

 def checkPassword(self, num):
  self.tempPassword += num
   
 def clearPassword(self):
  self.tempPassword = ""

 def enterPassword(self):
  if self.tempPassword == self.password :
    self.asignal.emit()
    self.tempPassword = ""
     
 def goBackHome(self):
  self.backH.emit()

 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)
 
  self.password = "1234"
  self.tempPassword = ""
  self.backHome.clicked.connect(lambda : self.goBackHome())
  self.zero.clicked.connect(lambda : self.checkPassword("0"))
  self.one.clicked.connect(lambda : self.checkPassword("1"))
  self.two.clicked.connect(lambda : self.checkPassword("2"))
  self.three.clicked.connect(lambda : self.checkPassword("3"))
  self.four.clicked.connect(lambda : self.checkPassword("4"))
  self.five.clicked.connect(lambda : self.checkPassword("5"))
  self.six.clicked.connect(lambda : self.checkPassword("6"))
  self.seven.clicked.connect(lambda : self.checkPassword("7"))
  self.eight.clicked.connect(lambda : self.checkPassword("8"))
  self.nine.clicked.connect(lambda : self.checkPassword("9"))
  self.clear.clicked.connect(lambda : self.clearPassword())
  self.enter.clicked.connect(lambda : self.enterPassword())
