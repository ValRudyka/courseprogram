# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'groupsKbkHcG.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1032, 684)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"    border-radius: 3px;\n"
"}")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(200, 180, 101, 41))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(490, 90, 101, 41))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(330, 180, 101, 41))
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 90, 421, 41))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(20, 50, 111, 21))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 141, 31))
        font = QFont()
        font.setFamily(u"Segoe UI")
        self.label.setFont(font)
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(70, 180, 101, 41))
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(20, 240, 981, 371))
        self.tableView.setGridStyle(Qt.SolidLine)
        self.tableView.setSortingEnabled(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1032, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0423\u0433\u0440\u0443\u043f\u043e\u0432\u0443\u0432\u0430\u043d\u043d\u044f", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u0442\u0438", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0431\u0456\u0440\u043a\u0430", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u043b\u0443\u0447\u0438\u0442\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u0435 \u0434\u043b\u044f \u0432\u0438\u0431\u0456\u0440\u043a\u0438", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438", None))
    # retranslateUi

