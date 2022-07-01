# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 480)
        Dialog.setStyleSheet("")
        self.maintenance = QtWidgets.QPushButton(Dialog)
        self.maintenance.setGeometry(QtCore.QRect(20, 60, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.maintenance.setFont(font)
        self.maintenance.setCheckable(True)
        self.maintenance.setObjectName("maintenance")
        self.restart = QtWidgets.QPushButton(Dialog)
        self.restart.setGeometry(QtCore.QRect(280, 60, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.restart.setFont(font)
        self.restart.setObjectName("restart")
        self.back = QtWidgets.QPushButton(Dialog)
        self.back.setGeometry(QtCore.QRect(540, 60, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.back.setFont(font)
        self.back.setStyleSheet("")
        self.back.setObjectName("back")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(240, 0, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.maintenance.toggled['bool'].connect(self.back.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.maintenance.setText(_translate("Dialog", "Maintenance"))
        self.restart.setText(_translate("Dialog", "Restart"))
        self.back.setText(_translate("Dialog", "Return"))
        self.label.setText(_translate("Dialog", "Admin Menu"))
