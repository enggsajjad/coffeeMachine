# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeMain.ui'
#
# Created: Sat Dec 10 20:43:03 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 480)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("background : rgb(217, 203, 174);\n"
"border: none;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.menu = QtWidgets.QWidget(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(0, 0, 141, 491))
        self.menu.setStyleSheet("background:rgb(72, 43, 27)")
        self.menu.setObjectName("menu")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.menu)
        self.lineEdit_2.setGeometry(QtCore.QRect(0, 0, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("color : white;\n"
"background-color : #3f2a14")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.commandLinkButton_2 = QtWidgets.QCommandLinkButton(self.menu)
        self.commandLinkButton_2.setGeometry(QtCore.QRect(30, 390, 81, 91))
        self.commandLinkButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.commandLinkButton_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.commandLinkButton_2.setStyleSheet(":hover { background-color : rgb(0,0,0,0)}")
        self.commandLinkButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/coffee.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_2.setIcon(icon)
        self.commandLinkButton_2.setIconSize(QtCore.QSize(80, 80))
        self.commandLinkButton_2.setObjectName("commandLinkButton_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.menu)
        self.pushButton_2.setGeometry(QtCore.QRect(-3, 50, 141, 31))
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pushButton_2.setStyleSheet("color : rgba(255,255,255,90);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../res/homeIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(15, 15))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.menu)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 100, 141, 31))
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_3.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pushButton_3.setStyleSheet("color : rgba(255,255,255,90);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../res/androidIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(15, 15))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_2.setText(_translate("MainWindow", "    Coffee Time"))
        self.pushButton_2.setText(_translate("MainWindow", "Main menu"))
        self.pushButton_3.setText(_translate("MainWindow", "Android app"))

