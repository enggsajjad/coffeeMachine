# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 480)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.stackedWidget.setObjectName("stackedWidget")
        self.get_uid_widget = GetUid()
        self.get_uid_widget.setObjectName("get_uid_widget")
        self.stackedWidget.addWidget(self.get_uid_widget)
        self.water_alert_widget = QtWidgets.QWidget()
        self.water_alert_widget.setObjectName("water_alert_widget")
        self.textEdit = QtWidgets.QTextEdit(self.water_alert_widget)
        self.textEdit.setGeometry(QtCore.QRect(80, 50, 641, 371))
        self.textEdit.setStyleSheet("background-color: #48b9ff;\n"
"border-radius: 12px;\n"
"padding-top: 12px;")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.water_alert_widget)
        self.label.setGeometry(QtCore.QRect(300, 150, 211, 151))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("res/ink-cartridge.svg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.stackedWidget.addWidget(self.water_alert_widget)
        self.got_user_widget = GotUser()
        self.got_user_widget.setObjectName("got_user_widget")
        self.stackedWidget.addWidget(self.got_user_widget)
        self.unregistered_uid_widget = UnregisteredUid()
        self.unregistered_uid_widget.setObjectName("unregistered_uid_widget")
        self.stackedWidget.addWidget(self.unregistered_uid_widget)
        self.admin_login_widget = AdminLogin()
        self.admin_login_widget.setObjectName("admin_login_widget")
        self.stackedWidget.addWidget(self.admin_login_widget)
        self.admin_widget = Admin()
        self.admin_widget.setObjectName("admin_widget")
        self.stackedWidget.addWidget(self.admin_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">Water tank is empty</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:36pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:36pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:36pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">Please refill</span></p></body></html>"))
from gui.admin import Admin
from gui.admin_login import AdminLogin
from gui.get_uid import GetUid
from gui.got_user import GotUser
from gui.unregistered_uid import UnregisteredUid
