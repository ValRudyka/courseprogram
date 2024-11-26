from mvc.view.main.ui_main import MainWindow
from PySide6.QtCore import QObject

class Controller(QObject):
    def __init__(self, main: MainWindow) -> None:
        self.main = main
        self.main.timer.timeout.connect(self.main.update_time)
        self.main.ui.pushButton.clicked.connect(self.toggle_theme)

    def toggle_theme(self) -> None:
        self.main.theme = 'dark' if self.main.theme == 'light' else 'light'
        
        self.main.set_theme()

