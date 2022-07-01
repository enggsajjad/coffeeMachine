# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_uid.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GetUid(object):
    def setupUi(self, GetUid):
        GetUid.setObjectName("GetUid")
        GetUid.resize(800, 480)
        GetUid.setStyleSheet("")
        self.frame = QtWidgets.QFrame(GetUid)
        self.frame.setGeometry(QtCore.QRect(-11, -10, 821, 91))
        self.frame.setStyleSheet("background-color: rgb(211, 215, 207);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.button_left = QtWidgets.QPushButton(self.frame)
        self.button_left.setGeometry(QtCore.QRect(20, 15, 71, 71))
        self.button_left.setText("")
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.button_left.setIcon(icon)
        self.button_left.setIconSize(QtCore.QSize(40, 40))
        self.button_left.setObjectName("button_left")
        self.button_reset = QtWidgets.QPushButton(self.frame)
        self.button_reset.setGeometry(QtCore.QRect(100, 15, 71, 71))
        self.button_reset.setText("")
        icon = QtGui.QIcon.fromTheme("edit-undo")
        self.button_reset.setIcon(icon)
        self.button_reset.setIconSize(QtCore.QSize(40, 40))
        self.button_reset.setObjectName("button_reset")
        self.button_right = QtWidgets.QPushButton(self.frame)
        self.button_right.setGeometry(QtCore.QRect(735, 15, 71, 71))
        self.button_right.setText("")
        icon = QtGui.QIcon.fromTheme("go-next")
        self.button_right.setIcon(icon)
        self.button_right.setIconSize(QtCore.QSize(40, 40))
        self.button_right.setObjectName("button_right")
        self.button_last = QtWidgets.QPushButton(self.frame)
        self.button_last.setGeometry(QtCore.QRect(655, 15, 71, 71))
        self.button_last.setText("")
        icon = QtGui.QIcon.fromTheme("go-last")
        self.button_last.setIcon(icon)
        self.button_last.setIconSize(QtCore.QSize(40, 40))
        self.button_last.setObjectName("button_last")
        self.admin_button = QtWidgets.QPushButton(self.frame)
        self.admin_button.setGeometry(QtCore.QRect(575, 15, 71, 71))
        self.admin_button.setText("")
        icon = QtGui.QIcon.fromTheme("preferences-system")
        self.admin_button.setIcon(icon)
        self.admin_button.setIconSize(QtCore.QSize(40, 40))
        self.admin_button.setObjectName("admin_button")
        self.text = QtWidgets.QTextEdit(self.frame)
        self.text.setEnabled(True)
        self.text.setGeometry(QtCore.QRect(260, 30, 291, 41))
        self.text.setStyleSheet("padding-top: 1px;")
        self.text.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text.setReadOnly(True)
        self.text.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.text.setObjectName("text")
        self.progressBar = QtWidgets.QProgressBar(GetUid)
        self.progressBar.setGeometry(QtCore.QRect(0, 65, 801, 20))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.raise_()
        self.frame.raise_()

        self.retranslateUi(GetUid)
        QtCore.QMetaObject.connectSlotsByName(GetUid)

    def retranslateUi(self, GetUid):
        _translate = QtCore.QCoreApplication.translate
        GetUid.setWindowTitle(_translate("GetUid", "Dialog"))
        self.text.setHtml(_translate("GetUid", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Almost ready!</span></p></body></html>"))
        self.progressBar.setFormat(_translate("GetUid", "%ps"))
