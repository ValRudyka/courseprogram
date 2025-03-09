from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow

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
            self.curr_view.hide()

        self.views[view_name].show()
        self.curr_view = view_name
