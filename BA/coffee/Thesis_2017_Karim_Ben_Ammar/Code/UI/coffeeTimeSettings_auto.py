# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoffeeTimeSettings.ui'
#
# Created: Wed Dec 14 09:48:40 2016
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
        self.lineEdit.setGeometry(QtCore.QRect(210, 30, 231, 51))
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
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(124, 214, 181, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(120, 264, 231, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.limitPerDay = QtWidgets.QSpinBox(Dialog)
        self.limitPerDay.setGeometry(QtCore.QRect(350, 204, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setUnderline(False)
        self.limitPerDay.setFont(font)
        self.limitPerDay.setFocusPolicy(QtCore.Qt.NoFocus)
        self.limitPerDay.setStyleSheet("border:  1px solid rgb(72,43,27)")
        self.limitPerDay.setObjectName("limitPerDay")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(350, 260, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBox.setFont(font)
        self.spinBox.setStyleSheet("border: 1px solid rgb(72, 43, 27)")
        self.spinBox.setObjectName("spinBox")
        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setGeometry(QtCore.QRect(480, 350, 97, 26))
        self.saveButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.saveButton.setStyleSheet("background : rgb(72, 43, 27);\n"
"border-radius: 10px;\n"
"color : white;")
        self.saveButton.setObjectName("saveButton")
        self.backButton = QtWidgets.QCommandLinkButton(Dialog)
        self.backButton.setGeometry(QtCore.QRect(600, 0, 41, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy)
        self.backButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.backButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.backButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/backIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(30, 30))
        self.backButton.setObjectName("backButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setText(_translate("Dialog", "      Settings"))
        self.lineEdit_2.setText(_translate("Dialog", "Coffee limit per day :"))
        self.lineEdit_3.setText(_translate("Dialog", "Coffee limit per month :"))
        self.saveButton.setText(_translate("Dialog", "Save"))

