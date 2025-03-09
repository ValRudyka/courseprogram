# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registernmORXi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_RegisterWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(561, 632)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(70, 30, 441, 71))
        font = QFont()
        font.setFamily(u"Nirmala UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(font.Weight.Normal)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setIndent(-2)
        self.username_edit = QLineEdit(self.centralwidget)
        self.username_edit.setObjectName(u"username_edit")
        self.username_edit.setGeometry(QRect(50, 200, 211, 31))
        font1 = QFont()
        font1.setFamily(u"Nirmala UI")
        font1.setPointSize(9)
        self.username_edit.setFont(font1)
        self.username_edit.setMaxLength(200)
        self.username_label = QLabel(self.centralwidget)
        self.username_label.setObjectName(u"username_label")
        self.username_label.setGeometry(QRect(50, 150, 211, 31))
        self.password_edit = QLineEdit(self.centralwidget)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setGeometry(QRect(50, 320, 211, 31))
        self.password_edit.setFont(font1)
        self.password_edit.setMaxLength(200)
        self.password_label = QLabel(self.centralwidget)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(50, 270, 211, 31))
        self.register_btn = QPushButton(self.centralwidget)
        self.register_btn.setObjectName(u"register_btn")
        self.register_btn.setGeometry(QRect(50, 390, 121, 51))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 480, 341, 61))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(390, 490, 101, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 561, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u044f", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0432\u043e\u0440\u0456\u0442\u044c \u043d\u043e\u0432\u043e\u0433\u043e \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430", None))
        self.username_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0430\u043a\u0430\u0443\u043d\u0442", None))
        self.username_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt;\">\u0412\u0432\u0435\u0434\u0456\u0442\u044c \u0456\u043c'\u044f \u0430\u043a\u0430\u0443\u043d\u0442\u0443:</span></p></body></html>", None))
        self.password_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"1234...", None))
        self.password_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt;\">\u0412\u0432\u0435\u0434\u0456\u0442\u044c \u0441\u0432\u0456\u0439 \u043f\u0430\u0440\u043e\u043b\u044c:</span></p></body></html>", None))
        self.register_btn.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0440\u0435\u0454\u0441\u0442\u0440\u0443\u0432\u0430\u0442\u0438\u0441\u044f", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt;\">\u0412\u0436\u0435 \u043c\u0430\u0454\u0442\u0435 \u0430\u043a\u0430\u0443\u043d\u0442? \u041f\u0435\u0440\u0435\u0439\u0434\u0456\u0442\u044c \u0434\u043e \u0432\u0456\u043a\u043d\u0430 \u0432\u0445\u043e\u0434\u0443</span></p></body></html>", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0445\u0456\u0434", None))
    # retranslateUi

