# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gang_editxceico.ui'
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
        MainWindow.resize(584, 468)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(40, 140, 151, 31))
        font = QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 50, 111, 31))
        self.label_2.setFont(font)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(310, 140, 151, 31))
        self.label_10.setFont(font)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(310, 50, 171, 31))
        self.label_11.setFont(font)
        self.label_34 = QLabel(self.centralwidget)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(310, 230, 151, 31))
        self.label_34.setFont(font)
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(40, 180, 141, 31))
        self.dateEdit.setInputMethodHints(Qt.ImhDate|Qt.ImhPreferNumbers)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QDate(2024, 11, 16))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(310, 340, 141, 41))
        self.pushButton_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(40, 230, 151, 31))
        self.label_9.setFont(font)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(40, 90, 141, 22))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(310, 90, 171, 22))
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(310, 270, 171, 22))
        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(310, 180, 171, 31))
        self.spinBox.setMinimum(1)
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(40, 270, 141, 31))
        self.comboBox.setEditable(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 584, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u043d\u043d\u044f \u0443\u0433\u0440\u0443\u043f\u043e\u0432\u0443\u0432\u0430\u043d\u043d\u044f", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430 \u0437\u0430\u0441\u043d\u0443\u0432\u0430\u043d\u043d\u044f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0432\u0430", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0447\u043b\u0435\u043d\u0456\u0432", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u043d\u043e\u0432\u043d\u0430 \u0434\u0456\u044f\u043b\u044c\u043d\u0456\u0441\u0442\u044c", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0443\u0441", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043d\u043e\u0432\u0438\u0442\u0438", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0456\u0441\u0446\u0435 \u0431\u0430\u0437\u0438", None))
    # retranslateUi

