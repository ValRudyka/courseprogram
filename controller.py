from view.main.ui_main import MainWindow
from PySide6.QtCore import QObject

class Controller(QObject):
    def __init__(self, main: MainWindow) -> None:
        self.main = main
        self.main.timer.timeout.connect(self.main.update_time)