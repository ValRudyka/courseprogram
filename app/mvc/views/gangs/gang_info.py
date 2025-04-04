from PySide6.QtWidgets import QMainWindow
from .gangs_source import Ui_MainWindow

class GangsView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)