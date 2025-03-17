from PySide6.QtWidgets import QMainWindow
from .archive_info import Ui_MainWindow

class CriminalsView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)