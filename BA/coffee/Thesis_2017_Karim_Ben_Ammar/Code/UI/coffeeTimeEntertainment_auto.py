# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeEntertainment.ui'
#
# Created: Sun Feb 12 13:56:28 2017
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
        self.nextButton = QtWidgets.QCommandLinkButton(Dialog)
        self.nextButton.setGeometry(QtCore.QRect(610, 400, 41, 41))
        self.nextButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nextButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/nextIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextButton.setIcon(icon)
        self.nextButton.setIconSize(QtCore.QSize(30, 30))
        self.nextButton.setObjectName("nextButton")
        self.predButton = QtWidgets.QCommandLinkButton(Dialog)
        self.predButton.setGeometry(QtCore.QRect(10, 400, 41, 41))
        self.predButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.predButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../res/backIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.predButton.setIcon(icon1)
        self.predButton.setIconSize(QtCore.QSize(30, 30))
        self.predButton.setObjectName("predButton")
        self.waiting = QtWidgets.QWidget(Dialog)
        self.waiting.setGeometry(QtCore.QRect(0, 0, 659, 401))
        self.waiting.setStyleSheet("background : rgb(217, 203, 174);\n"
"border: none;")
        self.waiting.setObjectName("waiting")
        self.lineEdit = QtWidgets.QLineEdit(self.waiting)
        self.lineEdit.setGeometry(QtCore.QRect(260, 200, 141, 27))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEdit.setFont(font)
        self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit.setStyleSheet("color:rgb(72,43,27)")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.image = QtWidgets.QLabel(Dialog)
        self.image.setGeometry(QtCore.QRect(0, 0, 659, 401))
        self.image.setText("")
        self.image.setObjectName("image")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setText(_translate("Dialog", "Loadging..."))

