from PySide6.QtCore import QObject, Slot

class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.main_view = None
        self.criminals_view = None
        self.groups_view = None
        self.archive_view = None
    
    def set_main_view(self, view):
        self.main_view = view
        
        self.main_view.open_criminals_requested.connect(self.show_criminals_view)
        self.main_view.open_groups_requested.connect(self.show_groups_view)
        self.main_view.open_archive_requested.connect(self.show_archive_view)
    
    def set_criminals_view(self, view):
        self.criminals_view = view
    
    def set_groups_view(self, view):
        self.groups_view = view
    
    def set_archive_view(self, view):
        self.archive_view = view
    
    @Slot()
    def handle_logout(self):
        pass
    
    @Slot()
    def show_criminals_view(self):
        if self.criminals_view:
            self.criminals_view.show()
    
    @Slot()
    def show_groups_view(self):
        if self.groups_view:
            pass
    
    @Slot()
    def show_archive_view(self):
        if self.archive_view:
            pass