from mvc.view.main.mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer

from time import localtime, strftime

import qdarktheme

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.__theme = 'light'
        self.ui.setupUi(self)
        self.set_theme()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.update_time()
    
    @property
    def theme(self) -> str:
        return self.__theme
    
    @theme.setter
    def theme(self, value: str) -> None:
        self.__theme = value

    def set_theme(self) -> None:
        qdarktheme(self.__theme)

        if self.__theme == "light":
            self.setStyleSheet( """ 
            QPushButton {
                background-color: #fff4e6;
                border-radius: 3px;               
            }
        """)

    def update_time(self) -> None:
        curr_time = strftime("%H:%M:%S", localtime())
        self.ui.label_2.setText(curr_time)

