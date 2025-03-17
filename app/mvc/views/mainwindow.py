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
        
        self.ui.menu_2.triggered.connect(self._on_criminals_menu)
        self.ui.menu_3.triggered.connect(self._on_groups_menu)
        self.ui.menu_4.triggered.connect(self._on_archive_menu)
        
        self.ui.pushButton_2.clicked.connect(self._on_add_criminal)
        self.ui.pushButton_3.clicked.connect(self._on_add_group)
        
    def _on_criminals_menu(self):
        self.open_criminals_requested.emit()
    
    def _on_groups_menu(self):
        self.open_groups_requested.emit()
    
    def _on_archive_menu(self):
        self.open_archive_requested.emit()
    
    def _on_add_criminal(self):
        self.open_criminals_requested.emit()
    
    def _on_add_group(self):
        self.open_groups_requested.emit()