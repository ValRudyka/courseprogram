from PySide6.QtWidgets import QMainWindow
from .criminals_source import Ui_CriminalsWindow

class CriminalsView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CriminalsWindow()
        self.ui.setupUi(self)