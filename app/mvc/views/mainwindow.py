from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal
from .main_source import Ui_MainWindow

class MainWindow(QMainWindow):
    open_criminals_requested = Signal()
    open_groups_requested = Signal()
    open_archive_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)        

        self.ui.pushButton_2.clicked.connect(self._on_criminals_action)
        self.ui.pushButton_3.clicked.connect(self._on_groups_action)
        

    def _on_criminals_action(self):
        self.open_criminals_requested.emit()

    def _on_groups_action(self):
        self.open_groups_requested.emit()

    def _on_archive_action(self):
        self.open_archive_requested.emit()
        
    def _on_add_criminal(self):
        self.open_criminals_requested.emit()
    
    def _on_add_group(self):
        self.open_groups_requested.emit()