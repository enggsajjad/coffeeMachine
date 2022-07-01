import sys
import os

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util import internet_on
from serverCommunication import passOrder
from dbHandler import addOfflineTransaction, getMilkChoice, setMilkChoice
import time
import multiprocessing
import errno

from serverCommunication import getUserInfo
from dbHandler import updateDB, getUser, handleOfflineTransactions
import coffeeTimeOrder_auto

class CoffeeTimeOrder(QDialog, coffeeTimeOrder_auto.Ui_Dialog):

    trigger = pyqtSignal(int)

    def chooseWithMilk(self):
        self.withMilk = True
        #if not os.path.isfile("/home/pi/CoffeeMachine/UI/withMilk.txt"):
            #with open("/home/pi/CoffeeMachine/UI/withMilk.txt", "w") as f:
            #    pass

    def chooseWithoutMilk(self):
        self.withMilk = False
        #if os.path.isfile("/home/pi/CoffeeMachine/UI/withMilk.txt"):
        #    os.remove("/home/pi/CoffeeMachine/UI/withMilk.txt")

    def newUser(self, uid):
        if os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/order.txt")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/stop.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/stop.txt")
        if not self.lockSession and not self.nowater:
            self.uid = ''
            self.firstOrder = True
            if uid == "69688e3b":
                self.uid = "0123"
            else:
                self.uid = uid
            if getMilkChoice(uid) :
                if getMilkChoice(uid) == 0:
                    self.radioWithMilk.setChecked(False)
                else :
                    self.radioWithMilk.setChecked(True)
            if internet_on():
                user = getUserInfo(self.uid).split(";")
                if len(user) >= 4:
                    self.token = user[4]
            else:
                temp = getUser(self.uid)
                user. append('')
                user. append(temp[0])
                user. append(temp[1])
            if len(user) > 2:
                self.user.setText(user[1])
                self.tempBalance = int(user[2])
                self.balance.setText(str(int(user[2]) / 100) + " €")
                # if int(user[2]) > 0:
                self.validUser = True
                with open("/home/pi/CoffeeMachine/UI/unlock.txt", "a") as f:
                    pass
                self.timerHandler()
                # else:
                #    os.remove("userUID.png")
                #    self.messageHandler(
                #        "Sorry you don't have enough balance. Please recharge your account first.")
            else:
                os.remove("/home/pi/CoffeeMachine/UI/userUID.png")
                #os.remove("/home/pi/CoffeeMachine/UI/uid.txt")
                self.uid = ""
                with open("invalidUser.txt", "a") as f:
                    pass
                self.messageHandler(
                    "Sorry this user is not registered. For further informations go to Marvin (room 314.4) or Farzad (Room 313.3). Your UID is %s" %uid, 5000)

    def messageHandler(self, message, sec):
        self.message.setText(message)
        self.message.setAlignment(Qt.AlignCenter)
        self.image.hide()
        self.message.show()
        self.scrollArea.hide()
        self.predButton.hide()
        self.nextButton.hide()
        QTimer.singleShot(sec, self.hideMessage)

    def hideMessage(self):
        self.message.setText("")
        self.scrollArea.show()
        self.image.show()
        self.message.hide()
        self.predButton.show()
        self.nextButton.show()

    def timerHandler(self):
        self.session = 30
        self.lockSession = True
        self.radioWithMilk.show()
        self.radioWithoutMilk.show()
        #self.flags[0] = 1
        self.qTimer = QTimer(self)
        self.qTimer.timeout.connect(self.updateTimer)
        self.qTimer.start(1500)

    def updateTimer(self):
        if self.session > 0:
            if os.path.isfile("/home/pi/CoffeeMachine/UI/stop.txt"):
                self.session = 0
                os.remove("/home/pi/CoffeeMachine/UI/stop.txt")
                self.updateTimer()
            else:
                self.trigger.emit(self.session)
                self.session = self.session - 1
        else:
            self.qTimer.stop()
            self.trigger.emit(self.session)
            self.lockSession = False
            self.user.setText("")
            self.balance.setText("")
            self.token = ""
            os.remove("/home/pi/CoffeeMachine/UI/userUID.png")
            if os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt"):
                os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")
            if not os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
                self.uid = ""
            #self.flags[0] = 0
            self.radioWithMilk.hide()
            self.radioWithoutMilk.hide()
            # if os.path.isfile("order.txt"):
            #     self.firstOrder = False
            #     if os.path.isfile("stop.txt"):
            #         os.remove("stop.txt")
            #     with open("order.txt") as f:
            #         choice = f.readline()
            #     if choice == "water\n":
            #         second = "true"
            #         self.tempBalance = self.tempBalance - 1
            #         self.messageHandler(
            #             "Thousands have lived without love, not one without water.")
            #         self.finalOrder.setText(
            #             "You ordered water. Your new balance is %s €" % str(self.tempBalance / 100))
            #     else:
            #         second = "false"
            #         self.messageHandler(
            #             "3 cups of coffee a day keeps the doctor away")
            #         if self.withMilk:
            #             self.tempBalance = self.tempBalance - 20
            #             first = "false"
            #         else:
            #             first = "true"
            #             self.tempBalance = self.tempBalance - 25
            #         self.finalOrder.setText(
            #             "You ordered coffee. Your new balance is %s €" % str(self.tempBalance / 100))
            #     if self.withMilk == False:
            #         first = "true"
            #     else:
            #         first = "false"
            #     if internet_on():
            #         passOrder(self.uid, first, second)
            #     else:
            #         addOfflineTransaction(self.uid, first, second)
            #     #QTimer.singleShot(1000, self.reLock)

    def secondOrder(self, choice):
            if os.path.isfile("/home/pi/CoffeeMachine/UI/lastOrder.txt"):
                file_mod_time = os.stat("/home/pi/CoffeeMachine/UI/lastOrder.txt").st_mtime
                last_time = (time.time() - file_mod_time) / 60
                if choice == "water\n" and last_time > self.sleepModeTime:
                    self.tempBalance = 0
            else:
                with open("/home/pi/CoffeeMachine/UI/lastOrder.txt", "a") as f:
                    pass
            if not self.tempBalance == 0:
                first = ''
                second = ''
                if os.path.isfile("/home/pi/CoffeeMachine/UI/done.txt"):
                    os.remove("/home/pi/CoffeeMachine/UI/done.txt")
                if choice == "water\n":
                    second = "true"
                    if self.tempBalance :
                        self.tempBalance = self.tempBalance - 1
                        self.messageHandler("You ordered water. Your new balance is %s €" % str(self.tempBalance / 100), 5000)
                else:
                    second = "false"
                    if self.withMilk:
                        if self.tempBalance :
                            self.tempBalance = self.tempBalance - 25
                        first = "false"
                        setMilkChoice(self.uid, 1)
                    else:
                        first = "true"
                        setMilkChoice(self.uid, 0)
                        if self.tempBalance :
                            self.tempBalance = self.tempBalance - 20
                            self.messageHandler("You ordered coffee. Your new balance is %s €" % str(self.tempBalance / 100), 5000)
                if internet_on():
                    #passOrder(self.uid, first, second)
                    try:
                        p = multiprocessing.Process(target=passOrder, args=(self.uid, first, second))
                        p.start()
                    except:
                        with open("/home/pi/logs/order.log", "a") as f:
                            f.write("Order error: %s \n" % sys.exc_info()[0])
                        pass
                else:
                    addOfflineTransaction(self.uid, first, second)
                if os.path.isfile("/home/pi/CoffeeMachine/lastOrder.txt"):
                    os.remove("/home/pi/CoffeeMachine/UI/lastOrder.txt")
                    with open("/home/pi/CoffeeMachine/UI/lastOrder.txt") as f:
                        pass
                self.tempBalance = 0

    def isFirstOrder(self):
        return self.firstOrder

    def getToken(self):
        return self.token

    def resetUID(self):
        self.uid = ''
        self.tempBalance = 0

    def reLock(self):
        with open("/home/pi/CoffeeMachine/UI/unlock.txt", "a") as f:
            pass
        QTimer.singleShot(2000, self.lockAgain)

    def lockAgain(self):
        os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")

    def predImage(self):
        self.index = (self.index - 1) % len(self.images)
        try :
            pixmap = QPixmap(self.images[self.index])
            if pixmap.width() > 800:
                pixmap.scaledToHeight(350)
            else:
                pixmap.scaledToWidth(650)
            self.image.setPixmap(pixmap)
        except :
            pass

    def nextImage(self):
        self.images = self.getImages()
        self.index = (self.index + 1) % len(self.images)
        try :
            pixmap = QPixmap(self.images[self.index])
            if pixmap.width() > 800:
                pixmap.scaledToHeight(350)
            else:
                pixmap.scaledToWidth(650)
            self.image.setPixmap(pixmap)
        except :
            pass

    def getImages(self):
        images = []
        for file in os.listdir("/home/pi/Pictures"):
            if not file.endswith(".py"):
                images.append("/home/pi/Pictures/" + file)
        return images

    def cancelSession(self):
        self.session = 0

    def noWater(self):
        self.image.hide()
        self.scrollArea.hide()
        self.message.show()
        self.message.setText("Please fill the water tank")
        self.nowater = True
        self.predButton.hide()
        self.nextButton.hide()

    def isWater(self):
        self.image.show()
        self.scrollArea.show()
        self.message.hide()
        self.message.setText("")
        self.nowater = False
        self.predButton.show()
        self.nextButton.show()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.uid = ''
        self.withMilk = False
        self.lockSession = False
        self.firstOrder = True
        self.tempBalance = 0
        #self.addMilk.clicked.connect(lambda: self.chooseMilk())
        self.images = self.getImages()
        self.index = 0
        self.scrollArea.setWidget(self.image)
        self.nowater = False
        self.token = ""
        self.radioWithMilk.toggled.connect(lambda: self.chooseWithMilk())
        self.radioWithoutMilk.toggled.connect(lambda: self.chooseWithoutMilk())
        self.radioWithMilk.hide()
        self.radioWithoutMilk.hide()

        self.sleepModeTime = 120

        #self.flags = sa.attach("shm://flags")

        pixmap = QPixmap(self.images[self.index])
        if pixmap.width() > 800:
            pixmap.scaledToHeight(350)
        else:
            pixmap.scaledToWidth(650)
        self.image.setPixmap(pixmap)
        self.image.setAlignment(Qt.AlignCenter)
        self.predButton.clicked.connect(lambda: self.predImage())
        self.nextButton.clicked.connect(lambda: self.nextImage())
