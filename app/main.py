from mvc.view.main.ui_main import MainWindow
from mvc.controller import Controller
from PySide6.QtWidgets import QApplication
import sys


app = QApplication()
window = MainWindow()
controller = Controller(window)
window.show()

sys.exit(app.exec())


