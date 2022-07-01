# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeTest.ui'
#
# Created: Tue May 16 10:25:11 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 483)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("background : rgb(217, 203, 174);\n"
"border: none;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(1, 0, 800, 430))
        self.stackedWidget.setObjectName("stackedWidget")
        self.orderPage = CoffeeTimeOrder()
        self.orderPage.setAcceptDrops(False)
        self.orderPage.setObjectName("orderPage")
        self.stackedWidget.addWidget(self.orderPage)
        self.androidPage = CoffeeTimeAndroid()
        self.androidPage.setObjectName("androidPage")
        self.stackedWidget.addWidget(self.androidPage)
        self.adminLoginPage = CoffeeTimeAdminLogin()
        self.adminLoginPage.setObjectName("adminLoginPage")
        self.stackedWidget.addWidget(self.adminLoginPage)
        self.settingsPage = CoffeeTimeSettings()
        self.settingsPage.setObjectName("settingsPage")
        self.stackedWidget.addWidget(self.settingsPage)
        self.adminPage = CoffeeTimeAdmin()
        self.adminPage.setObjectName("adminPage")
        self.stackedWidget.addWidget(self.adminPage)
        self.accountingPage = CoffeeTimeAccounting()
        self.accountingPage.setObjectName("accountingPage")
        self.stackedWidget.addWidget(self.accountingPage)
        self.entertainementPage = QtWidgets.QWidget()
        self.entertainementPage.setObjectName("entertainementPage")
        self.stackedWidget.addWidget(self.entertainementPage)
        self.adminSettings = CoffeeTimeAdminSettings()
        self.adminSettings.setObjectName("adminSettings")
        self.stackedWidget.addWidget(self.adminSettings)
        self.machineState = QtWidgets.QLineEdit(self.centralwidget)
        self.machineState.setGeometry(QtCore.QRect(140, 430, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.machineState.setFont(font)
        self.machineState.setStyleSheet("color : rgb(72, 43, 27)")
        self.machineState.setText("")
        self.machineState.setAlignment(QtCore.Qt.AlignCenter)
        self.machineState.setReadOnly(True)
        self.machineState.setObjectName("machineState")
        self.cancelButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(70, 420, 71, 71))
        self.cancelButton.setStyleSheet("background:none")
        self.cancelButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/cancel-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon)
        self.cancelButton.setIconSize(QtCore.QSize(50, 50))
        self.cancelButton.setObjectName("cancelButton")
        self.androidMenu = QtWidgets.QPushButton(self.centralwidget)
        self.androidMenu.setGeometry(QtCore.QRect(350, 440, 40, 40))
        self.androidMenu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.androidMenu.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.androidMenu.setStyleSheet("color : rgba(255,255,255,90);")
        self.androidMenu.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../res/androidIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.androidMenu.setIcon(icon1)
        self.androidMenu.setIconSize(QtCore.QSize(31, 31))
        self.androidMenu.setObjectName("androidMenu")
        self.adminMenu = QtWidgets.QPushButton(self.centralwidget)
        self.adminMenu.setGeometry(QtCore.QRect(440, 440, 40, 40))
        self.adminMenu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.adminMenu.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.adminMenu.setStyleSheet("color : rgba(255,255,255,90);")
        self.adminMenu.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../res/adminIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.adminMenu.setIcon(icon2)
        self.adminMenu.setIconSize(QtCore.QSize(31, 31))
        self.adminMenu.setObjectName("adminMenu")
        self.accountingMenu = QtWidgets.QPushButton(self.centralwidget)
        self.accountingMenu.setGeometry(QtCore.QRect(510, 440, 40, 40))
        self.accountingMenu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.accountingMenu.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.accountingMenu.setStyleSheet("color : rgba(255,255,255,90);")
        self.accountingMenu.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../res/accountingIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.accountingMenu.setIcon(icon3)
        self.accountingMenu.setIconSize(QtCore.QSize(31, 31))
        self.accountingMenu.setObjectName("accountingMenu")
        self.mainMenu = QtWidgets.QPushButton(self.centralwidget)
        self.mainMenu.setGeometry(QtCore.QRect(270, 440, 40, 40))
        self.mainMenu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainMenu.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.mainMenu.setStyleSheet("color : rgba(255,255,255,90);")
        self.mainMenu.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../res/homeIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainMenu.setIcon(icon4)
        self.mainMenu.setIconSize(QtCore.QSize(31, 31))
        self.mainMenu.setObjectName("mainMenu")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

from coffeetimeorder import CoffeeTimeOrder
from coffeetimeaccounting import CoffeeTimeAccounting
from coffeetimeandroid import CoffeeTimeAndroid
from coffeetimeadminlogin import CoffeeTimeAdminLogin
from coffeetimeadmin import CoffeeTimeAdmin
from coffeetimeadminsettings import CoffeeTimeAdminSettings
from coffeetimesettings import CoffeeTimeSettings
