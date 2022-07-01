import sys
import os

import atexit
import multiprocessing

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSlot
from removeScreenSaver import wakeUP
import subprocess
import coffeeTimeTest_auto

class MainWindow(QMainWindow, coffeeTimeTest_auto.Ui_MainWindow):

    def exitApp(self):
        QApplication.quit()

    def loadPage(self, page):
        if page is "order":
            self.stackedWidget.setCurrentIndex(0)
        elif page is "android":
            self.stackedWidget.setCurrentIndex(1)
        elif page is "adminLogin":
            self.stackedWidget.setCurrentIndex(2)
        elif page is "admin":
            self.stackedWidget.setCurrentIndex(4)
        elif page is "accounting":
            self.stackedWidget.widget(5).updateAccounting(self.stackedWidget.widget(0).getToken().strip())
            self.stackedWidget.setCurrentIndex(5)

    def getUID(self):
        if os.path.isfile("/home/pi/CoffeeMachine/UI/uid.txt"):
            with open("/home/pi/CoffeeMachine/UI/uid.txt", "r+") as f:
                tempUID = f.readline()
            if tempUID == "88452ff" and not os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt") and not os.path.isfile("/home/pi/CoffeeMachine/UI/maintenance.txt"):
                with open("/home/pi/CoffeeMachine/UI/unlock.txt", "a") as f:
                    pass
                with open("/home/pi/CoffeeMachine/UI/maintenance.txt") as f:
                    pass
            elif tempUID == "88452ff" and os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt"):
                os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")
                if os.path.isfile("/home/pi/CoffeeMachine/UI/maintenance.txt"):
                    os.remove("/home/pi/CoffeeMachine/UI/maintenance.txt")
            else :
                self.stackedWidget.widget(0).newUser(tempUID)
                self.cancelButton.show()
            os.remove("/home/pi/CoffeeMachine/UI/uid.txt")
            #subprocess.call("sudo python removeScreenSaver.py")
        elif os.path.isfile("/home/pi/CoffeeMachine/UI/invalidUser.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/invalidUser.txt")
            self.cancelButton.hide()
        if os.path.isfile("/home/pi/CoffeeMachine/UI/nowater.txt") and self.nowater == False:
            self.stackedWidget.widget(0).noWater()
            self.nowater = True
        elif not os.path.isfile("/home/pi/CoffeeMachine/UI/nowater.txt") and self.nowater:
            self.stackedWidget.widget(0).isWater()
            self.nowater = False
        elif os.path.isfile("/home/pi/CoffeeMachine/UI/done.txt") and os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
            if os.path.isfile("/home/pi/CoffeeMachine/UI/uid.txt"):
                os.remove("/home/pi/CoffeeMachine/UI/uid.txt")
            with open("/home/pi/CoffeeMachine/UI/order.txt", "r") as f:
                temp = f.readlines()
                # if len(temp) > 1 :
                #     if temp[1] == "coffee":
                #         self.stackedWidget.widget(0).secondOrder(temp[1])
                # elif len(temp) == 1 and self.stackedWidget.widget(0).isFirstOrder():
                #     self.stackedWidget.widget(0).secondOrder(temp[0])
            os.remove("/home/pi/CoffeeMachine/UI/order.txt")
            for order in temp:
                with open("/home/pi/CoffeeMachine/UI/blabla.txt", "a") as f:
                    f.write(order)
                self.stackedWidget.widget(0).secondOrder(order)
            #os.remove("/home/pi/CoffeeMachine/UI/order.txt")
            self.stackedWidget.widget(0).resetUID()

    @pyqtSlot(int)
    def updateState(self, value):
        if value > 0:
            self.machineState.setText("%d s" % value)
            if not self.accountingMenu.isVisible():
                self.accountingMenu.show()
        else:
            self.machineState.setText("")
            self.cancelButton.hide()
            self.accountingMenu.hide()
            self.stackedWidget.setCurrentIndex(0)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mainMenu.clicked.connect(lambda: self.loadPage("order"))
        self.androidMenu.clicked.connect(lambda: self.loadPage("android"))
        self.adminMenu.clicked.connect(lambda: self.loadPage("adminLogin"))
        self.accountingMenu.clicked.connect(
            lambda: self.loadPage("accounting"))

        self.accountingMenu.hide()
        self.cancelButton.clicked.connect(
            lambda: self.stackedWidget.widget(0).cancelSession())
        self.machineState.setText("")
        self.cancelButton.hide()

        admin = self.stackedWidget.widget(2)
        admin.asignal.connect(lambda: self.loadPage("admin"))
        adminPage = self.stackedWidget.widget(4)
        adminPage.asignal.connect(lambda: self.exitApp())
        #adminPage.logSettings.connect(lambda: self.loadPage("adminSettings"))
        admin.backH.connect(lambda: self.loadPage("order"))
        order = self.stackedWidget.widget(0)
        order.trigger.connect(self.updateState)
        self.nowater = False

        if os.path.isfile("/home/pi/CoffeeMachine/UI/userUID.png"):
            os.remove("/home/pi/CoffeeMachine/UI/userUID.png")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/uid.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/uid.txt")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/done.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/done.txt")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/stop.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/stop.txt")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/order.txt")
        if os.path.isfile("/home/pi/CoffeeMachine/UI/maintenance.txt"):
            os.remove("/home/pi/CoffeeMachine/UI/maintenance.txt")
        QTimer.singleShot(1000, self.reLock)

        timer = QTimer(self)
        timer.timeout.connect(self.getUID)
        timer.start(1000)
        with open("/home/pi/CoffeeMachine/UI/lastOrder.txt", "a") as f:
            pass 
    def reLock(self):
        with open("/home/pi/CoffeeMachine/UI/unlock.txt", "a") as f :
            f.close()
        QTimer.singleShot(2000, self.lockAgain)

    def lockAgain(self):
        os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")

def end_app():
    if os.path.isfile("/home/pi/CoffeeMachine/UI/userUID.png"):
        os.remove("/home/pi/CoffeeMachine/UI/userUID.png")
    if os.path.isfile("/home/pi/CoffeeMachine/UI/unlock.txt"):
        os.remove("/home/pi/CoffeeMachine/UI/unlock.txt")
    if os.path.isfile("/home/pi/CoffeeMachine/UI/stop.txt"):
        os.remove("/home/pi/CoffeeMachine/UI/stop.txt")
    if os.path.isfile("/home/pi/CoffeeMachine/UI/order.txt"):
        os.remove("/home/pi/CoffeeMachine/UI/order.txt")
    #sa.delete("coffeeMachine")

def main():

    app = QApplication(sys.argv)
    form = MainWindow()
    form.showFullScreen()
    atexit.register(end_app)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
