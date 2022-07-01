import sys
import os

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from urllib.request import urlopen
from PyQt5.QtCore import *
# from PyQt5.QtWebKit import *
# from PyQt5.QtWebKitWidgets import *

import coffeeTimeEntertainment_auto

class CoffeeTimeEntertainment(QDialog, coffeeTimeEntertainment_auto.Ui_Dialog):

 # def getLinks(self):
 #  response = urlopen('http://i80misc01.itec.kit.edu/cybercoffee_entertainment/linklist')
 #  temp = response.read().decode('utf-8').split('\n')[2:]
 #  del temp[-1]
 #  links = [x.split(';')[1] for x in temp]
 #  links = [x.strip(' ') for x in links]
 #  return links
 #
 def predImage(self):
  self.index = (self.index - 1) % len(self.images)
  # self.view.load(QUrl(self.links[self.index]))
  pixmap = QPixmap(self.images[self.index]).scaled(659, 401, Qt.KeepAspectRatio)
  self.image.setPixmap(pixmap)
  #self.waiting.show()

 def nextImage(self):
  self.images = self.getImages()
  self.index = (self.index + 1) % len(self.images)
  # self.view.load(QUrl(self.links[self.index]))
  pixmap = QPixmap(self.images[self.index]).scaled(659, 401, Qt.KeepAspectRatio)
  self.image.setPixmap(pixmap)
  #self.waiting.show()

 def getImages(self):
     images = []
     for file in os.listdir("/home/pi/Pictures"):
         if not file.endswith(".py"):
             images.append("/home/pi/Pictures/" + file)
     return images

 def showMe(self):
  self.waiting.hide()

 def __init__(self):
  super(self.__class__, self).__init__()
  self.setupUi(self)
  # self.links = self.getLinks()
  # self.view = QWebView(self.widget)
  # self.view.setFixedWidth(659)
  self.images = self.getImages()
  self.index = 0
  self.image.setPixmap(QPixmap(self.images[self.index]).scaled(659, 401, Qt.KeepAspectRatio))
  self.waiting.hide()
  # self.view.load(QUrl(self.links[self.index]))
  # self.view.loadFinished.connect(lambda: self.showMe())
  self.predButton.clicked.connect(lambda: self.predImage())
  self.nextButton.clicked.connect(lambda: self.nextImage())
