# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'criminalsjwqCnX.ui'
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
        MainWindow.resize(1045, 540)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(255, 255, 255);\n"
"    border-radius: 3px;\n"
"}")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(520, 90, 111, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 40, 111, 31))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(30, 90, 111, 31))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(160, 90, 341, 31))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(680, 80, 101, 41))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(860, 20, 101, 41))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(860, 80, 101, 41))
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(680, 20, 101, 41))
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(30, 150, 961, 351))
        self.tableView.setSortingEnabled(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0417\u043b\u043e\u0447\u0438\u043d\u0446\u0456", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0456\u0440\u043a\u0430", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0456\u0440\u043a\u0430 \u0437\u0430 \u043f\u043e\u043b\u0435\u043c", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0440\u0445\u0456\u0432\u0443\u0432\u0430\u0442\u0438", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u043b\u0443\u0447\u0438\u0442\u0438", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438", None))
    # retranslateUi

