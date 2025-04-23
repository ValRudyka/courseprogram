# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'usersyAITIX.ui'
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
        MainWindow.resize(682, 669)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(20, 150, 561, 431))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(370, 80, 141, 41))
        self.pushButton_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(370, 10, 141, 41))
        self.pushButton_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 261, 31))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(30, 60, 291, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 682, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434\u0430\u043b\u0438\u0442\u0438", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0440\u0435\u0454\u0441\u0442\u0440\u0443\u0432\u0430\u0442\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0417\u043d\u0430\u0439\u0442\u0438 \u0437\u0430 \u043b\u043e\u0433\u0456\u043d\u043e\u043c", None))
    # retranslateUi

