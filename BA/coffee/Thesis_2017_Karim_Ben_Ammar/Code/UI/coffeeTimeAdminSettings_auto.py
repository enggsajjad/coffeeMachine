# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeAdminSettings.ui'
#
# Created: Sun Feb 12 14:11:01 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(659, 480)
        Dialog.setStyleSheet("background : rgb(217, 203, 174);\n"
"border: none;")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(170, 30, 291, 51))
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
"color : rgb(72, 43, 27)")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.backButton = QtWidgets.QCommandLinkButton(Dialog)
        self.backButton.setGeometry(QtCore.QRect(600, 10, 41, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy)
        self.backButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.backButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.backButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/pi/CoffeeMachine/res/backIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setObjectName("backButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setText(_translate("Dialog", "       Admin settings   "))

