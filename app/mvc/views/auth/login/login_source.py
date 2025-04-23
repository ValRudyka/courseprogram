# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginkrkJmg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(624, 643)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.username_edit = QLineEdit(self.centralwidget)
        self.username_edit.setObjectName(u"username_edit")
        self.username_edit.setGeometry(QRect(60, 200, 211, 31))
        font = QFont()
        font.setFamily(u"Nirmala UI")
        font.setPointSize(9)
        self.username_edit.setFont(font)
        self.username_edit.setMaxLength(200)
        self.password_label = QLabel(self.centralwidget)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(60, 270, 211, 31))
        self.username_label = QLabel(self.centralwidget)
        self.username_label.setObjectName(u"username_label")
        self.username_label.setGeometry(QRect(60, 150, 211, 31))
        self.login_btn = QPushButton(self.centralwidget)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setGeometry(QRect(60, 390, 111, 41))
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(80, 30, 441, 71))
        font1 = QFont()
        font1.setFamily(u"Nirmala UI")
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setWeight(50)
        self.title.setFont(font1)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setIndent(-2)
        self.password_edit = QLineEdit(self.centralwidget)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setGeometry(QRect(60, 320, 211, 31))
        self.password_edit.setFont(font)
        self.password_edit.setMaxLength(200)
        self.password_edit.setEchoMode(QLineEdit.Password)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 624, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0445\u0456\u0434 \u0432 \u0441\u0438\u0441\u0442\u0435\u043c\u0443", None))
        self.username_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0430\u043a\u0430\u0443\u043d\u0442", None))
        self.password_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt;\">\u0412\u0432\u0435\u0434\u0456\u0442\u044c \u0441\u0432\u0456\u0439 \u043f\u0430\u0440\u043e\u043b\u044c:</span></p></body></html>", None))
        self.username_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt;\">\u0412\u0432\u0435\u0434\u0456\u0442\u044c \u0456\u043c'\u044f \u0430\u043a\u0430\u0443\u043d\u0442\u0443:</span></p></body></html>", None))
        self.login_btn.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0432\u0456\u0439\u0442\u0438", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0432\u0456\u0439\u0434\u0456\u0442\u044c \u0432 \u0441\u0438\u0441\u0442\u0435\u043c\u0443 \u0437\u0456 \u0441\u0432\u043e\u0433\u043e \u0430\u043a\u0430\u0443\u043d\u0442\u0443", None))
        self.password_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"*******", None))
    # retranslateUi

