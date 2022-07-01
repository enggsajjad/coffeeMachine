import sys

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *

import coffeeTimeAccounting_auto

class CoffeeTimeAccounting(QWebView, coffeeTimeAccounting_auto.Ui_Dialog):

 def updateAccounting(self, token):
     self.load(QUrl("http://i80misc01.ira.uka.de/coffee/kasse.php?token=" + token))
 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)
  self.setZoomFactor(0.85)
  #self.load(QUrl("http://i80misc01.ira.uka.de/coffee/kasse.php?token=C0FFE"))
