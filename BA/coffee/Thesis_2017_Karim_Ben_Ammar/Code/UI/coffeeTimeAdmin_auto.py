# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeAdmin.ui'
#
# Created: Tue May 16 09:17:17 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 430)
        Dialog.setStyleSheet("background : rgb(217, 203, 174)")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(280, 30, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit.setStyleSheet("border : 3px solid rgb(71,43,27);\n"
"border-radius : 10px;\n"
"background-color : rgb(217, 203, 174);\n"
"color : rgb(72, 43, 27);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.cleaningMode = QtWidgets.QCommandLinkButton(Dialog)
        self.cleaningMode.setGeometry(QtCore.QRect(220, 160, 125, 167))
        self.cleaningMode.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cleaningMode.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.cleaningMode.setStyleSheet(":hover { background-color : rgb(0,0,0,0)}")
        self.cleaningMode.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/pi/CoffeeMachine/res/cleaningNotSelected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cleaningMode.setIcon(icon)
        self.cleaningMode.setIconSize(QtCore.QSize(110, 150))
        self.cleaningMode.setObjectName("cleaningMode")
        self.exitFullscreen = QtWidgets.QCommandLinkButton(Dialog)
        self.exitFullscreen.setGeometry(QtCore.QRect(450, 160, 125, 167))
        self.exitFullscreen.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exitFullscreen.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.exitFullscreen.setStyleSheet(":hover { background-color : rgb(0,0,0,0)}")
        self.exitFullscreen.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/home/pi/CoffeeMachine/res/exitNotSelected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitFullscreen.setIcon(icon1)
        self.exitFullscreen.setIconSize(QtCore.QSize(110, 150))
        self.exitFullscreen.setObjectName("exitFullscreen")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setText(_translate("Dialog", "Admin"))

