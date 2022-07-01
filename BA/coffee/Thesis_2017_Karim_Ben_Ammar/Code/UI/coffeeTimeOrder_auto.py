# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeOrder.ui'
#
# Created: Tue May 16 10:20:24 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 430)
        Dialog.setStyleSheet("background : rgb(217, 203, 174);\n"
"border: none;")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 11, 181, 61))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.balance = QtWidgets.QLineEdit(Dialog)
        self.balance.setGeometry(QtCore.QRect(93, 45, 151, 27))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.balance.setFont(font)
        self.balance.setStyleSheet("background-color : transparent")
        self.balance.setText("")
        self.balance.setReadOnly(True)
        self.balance.setObjectName("balance")
        self.user = QtWidgets.QLineEdit(Dialog)
        self.user.setGeometry(QtCore.QRect(70, 10, 221, 27))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.user.setFont(font)
        self.user.setStyleSheet("background-color : transparent")
        self.user.setText("")
        self.user.setReadOnly(True)
        self.user.setObjectName("user")
        self.message = QtWidgets.QTextEdit(Dialog)
        self.message.setGeometry(QtCore.QRect(230, 140, 351, 171))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setStyleSheet("background : white;\n"
"border : 2px solid rgb(72, 43, 27);")
        self.message.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.message.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.message.setReadOnly(True)
        self.message.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.message.setPlaceholderText("")
        self.message.setObjectName("message")
        self.image = QtWidgets.QLabel(Dialog)
        self.image.setGeometry(QtCore.QRect(0, 80, 800, 311))
        self.image.setText("")
        self.image.setObjectName("image")
        self.predButton = QtWidgets.QCommandLinkButton(Dialog)
        self.predButton.setGeometry(QtCore.QRect(0, 385, 45, 45))
        self.predButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.predButton.setStyleSheet("background-color:transparent;\n"
"")
        self.predButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/pi/CoffeeMachine/res/backIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.predButton.setIcon(icon)
        self.predButton.setIconSize(QtCore.QSize(40, 40))
        self.predButton.setObjectName("predButton")
        self.nextButton = QtWidgets.QCommandLinkButton(Dialog)
        self.nextButton.setGeometry(QtCore.QRect(755, 385, 45, 45))
        self.nextButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.nextButton.setStyleSheet("background-color:transparent;\n"
"")
        self.nextButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/home/pi/CoffeeMachine/res/nextIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextButton.setIcon(icon1)
        self.nextButton.setIconSize(QtCore.QSize(40, 40))
        self.nextButton.setObjectName("nextButton")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(0, 80, 801, 311))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 801, 311))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.image2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image2.setGeometry(QtCore.QRect(0, 0, 800, 311))
        self.image2.setText("")
        self.image2.setObjectName("image2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.radioWithMilk = QtWidgets.QRadioButton(Dialog)
        self.radioWithMilk.setGeometry(QtCore.QRect(650, 10, 140, 22))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.radioWithMilk.setFont(font)
        self.radioWithMilk.setObjectName("radioWithMilk")
        self.radioWithoutMilk = QtWidgets.QRadioButton(Dialog)
        self.radioWithoutMilk.setGeometry(QtCore.QRect(440, 10, 171, 22))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.radioWithoutMilk.setFont(font)
        self.radioWithoutMilk.setChecked(True)
        self.radioWithoutMilk.setObjectName("radioWithoutMilk")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">User : </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Balance : </span></p></body></html>"))
        self.message.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:400;\"><br /></p></body></html>"))
        self.radioWithMilk.setText(_translate("Dialog", "With Milk"))
        self.radioWithoutMilk.setText(_translate("Dialog", "Without Milk"))

