from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QTimer, QDateTime, QLocale
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
        self.ui.pushButton_4.clicked.connect(self._on_archive_action)
        
        self.setup_time_display()
    
    def setup_time_display(self):
        """Set up the timer to update the date and time display."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.ukrainian_locale = QLocale(QLocale.Ukrainian, QLocale.Ukraine)
        
        self.update_time()
    
    def update_time(self):
        """Update the time display with current date and time in Ukrainian format."""
        now = QDateTime.currentDateTime()
        
        day_name = self.ukrainian_locale.toString(now, "dddd")
        day_number = now.toString("d")
        month_name = self.ukrainian_locale.toString(now, "MMMM")
        
        date_text = f"{day_name}, {day_number} {month_name}"
        
        time_text = now.toString("HH:mm:ss")
        
        full_text = f"{date_text}\n{time_text}"
        
        self.ui.label_2.setText(full_text)

    def closeEvent(self, event):
        """Handle window close event to properly clean up timer."""
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()

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