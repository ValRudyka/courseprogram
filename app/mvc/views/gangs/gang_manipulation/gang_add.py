# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gangs_manipulationHmvPIS.ui'
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
        MainWindow.resize(517, 425)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(290, 310, 141, 41))
        self.pushButton_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius: 3px;")
        self.lineEdit_9 = QLineEdit(self.centralwidget)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setGeometry(QRect(20, 60, 141, 22))
        self.label_35 = QLabel(self.centralwidget)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(290, 200, 151, 31))
        font = QFont()
        font.setPointSize(10)
        self.label_35.setFont(font)
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(20, 110, 151, 31))
        self.label_12.setFont(font)
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(20, 200, 151, 31))
        self.label_13.setFont(font)
        self.lineEdit_10 = QLineEdit(self.centralwidget)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setGeometry(QRect(290, 240, 141, 22))
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(290, 20, 241, 31))
        self.label_14.setFont(font)
        self.lineEdit_11 = QLineEdit(self.centralwidget)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setGeometry(QRect(290, 60, 151, 22))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 20, 111, 31))
        self.label_3.setFont(font)
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(290, 110, 211, 31))
        self.label_15.setFont(font)
        self.comboBox_7 = QComboBox(self.centralwidget)
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setGeometry(QRect(20, 240, 141, 21))
        self.comboBox_7.setEditable(True)
        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(20, 160, 141, 31))
        self.dateEdit.setInputMethodHints(Qt.ImhDate|Qt.ImhPreferNumbers)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QDate(2024, 11, 16))
        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(290, 150, 151, 31))
        self.spinBox.setMinimum(1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 517, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0420\u043e\u0431\u043e\u0442\u0430 \u0437 \u0437\u0430\u043f\u0438\u0441\u0430\u043c\u0438 \u0443\u0433\u0440\u0443\u043f\u043e\u0432\u0443\u0432\u0430\u043d\u044c", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0434\u0430\u0442\u0438", None))
        self.lineEdit_9.setPlaceholderText("")
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0443\u0441", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430 \u0437\u0430\u0441\u043d\u0443\u0432\u0430\u043d\u043d\u044f", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0456\u0441\u0446\u0435 \u0431\u0430\u0437\u0438", None))
        self.lineEdit_10.setPlaceholderText("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u043d\u043e\u0432\u043d\u0430 \u0434\u0456\u044f\u043b\u044c\u043d\u0456\u0441\u0442\u044c", None))
        self.lineEdit_11.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0437\u0432\u0430", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0456\u043b\u044c\u043a\u0456\u0441\u0442\u044c \u0447\u043b\u0435\u043d\u0456\u0432", None))
    # retranslateUi

