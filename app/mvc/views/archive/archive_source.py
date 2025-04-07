# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'archiveVnAgUC.ui'
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
        MainWindow.resize(1053, 615)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QPushButton {\n"
" \n"
"	background-color: rgb(255, 255, 255);\n"
"    border-radius: 3px;\n"
"}")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(20, 180, 1011, 371))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(660, 120, 121, 41))
        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(480, 120, 141, 41))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 10, 541, 71))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1053, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0410\u0440\u0445\u0456\u0432", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u043b\u0443\u0447\u0438\u0442\u0438", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0445\u043e\u0432\u0430\u0442\u0438 \u0444\u0456\u043b\u044c\u0442\u0440\u0438", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0433\u0430\u0434\u0443\u0432\u0430\u043d\u043d\u044f: \u0434\u0430\u043d\u0456 \u0437 \u0430\u0440\u0445\u0456\u0432\u0443 \u0432\u0438\u0434\u0430\u043b\u044f\u044e\u0442\u044c\u0441\u044f \u0447\u0435\u0440\u0435\u0437 2 \u0440\u043e\u043a\u0438 \u043f\u0456\u0441\u043b\u044f \u0434\u043e\u0434\u0430\u043d\u043d\u044f \u0456\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0456\u0457 \u043f\u0440\u043e \u0437\u043b\u043e\u0447\u0438\u043d\u0446\u044f. \u0422\u0430\u043a\u043e\u0436 \u043c\u043e\u0436\u043d\u0430 \u0432\u0438\u043b\u0443\u0447\u0438\u0442\u0438 \u0434\u0430\u043d\u0456 \u0432\u0440\u0443\u0447\u043d\u0443 ", None))
    # retranslateUi

