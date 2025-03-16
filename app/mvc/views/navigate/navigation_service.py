from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow
from mvc.views.mainwindow import MainWindow

class NavigationService(QObject):
    def __init__(self):
        super().__init__()
        self.curr_view = None
        self.views = {}
        self.main_window = None

    def register_view(self, view_name: str, view: QMainWindow) -> None:
        self.views[view_name] = view

    def show_view(self, view_name: str) -> None:
        if view_name not in self.views:
            return
        
        if self.curr_view:
            self.views[self.curr_view].hide()

        self.views[view_name].show()
        self.curr_view = view_name

    def show_main_window(self) -> None:
        if not self.main_window or not self.main_window.isVisible():
           self.main_window = MainWindow()

        self.main_window.show()
