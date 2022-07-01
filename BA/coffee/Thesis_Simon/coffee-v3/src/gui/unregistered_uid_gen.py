# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unregistered_uid.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 430)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(70, 20, 641, 231))
        self.textEdit.setStyleSheet("background-color: orange;\n"
"border-radius: 12px;\n"
"padding-top: 12px")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit.setObjectName("textEdit")
        self.button = QtWidgets.QPushButton(Dialog)
        self.button.setGeometry(QtCore.QRect(500, 280, 211, 121))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.button.setFont(font)
        self.button.setIconSize(QtCore.QSize(46, 46))
        self.button.setObjectName("button")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 280, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.uid = QtWidgets.QLabel(Dialog)
        self.uid.setGeometry(QtCore.QRect(90, 340, 391, 41))
        self.uid.setStyleSheet("font-size: 40px;")
        self.uid.setObjectName("uid")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Sorry this user is not registered.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">For further information go to </span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Sajjad Hussain (Room 315.4).</span></p>\n"
"</body></html>"))
        self.button.setText(_translate("Dialog", "Dismiss"))
        self.label.setText(_translate("Dialog", "Your UID is"))
        self.uid.setText(_translate("Dialog", "TextLabel"))
