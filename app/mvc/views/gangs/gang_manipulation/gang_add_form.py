from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal, QDate
from .gang_add import Ui_MainWindow
from utils.spinbox_utils import safe_get_spinbox_value

class GangAddForm(QMainWindow):
    save_requested = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setup_connections()
        self.reset_form()
    
    def setup_connections(self):
        """Connect UI elements to their corresponding actions."""
        self.ui.pushButton_3.clicked.connect(self.on_save)
    
    def load_reference_data(self, cities):
        """Load city data for location selection."""
        self.ui.comboBox_7.clear()
        
        for city in cities:
            display_text = f"{city['name']}, {city['country']}"
            self.ui.comboBox_7.addItem(display_text, city['id'])
    
    def on_save(self):
        """Handle save button click."""
        if not self.validate_form():
            return
        
        data = self.collect_form_data()
        
        self.save_requested.emit(data)
    
    def validate_form(self):
        """Validate form input before saving."""
        if not self.ui.lineEdit_9.text().strip():
            QMessageBox.warning(self, "Помилка валідації", "Назва є обов'язковою")
            return False
        
        return True
    
    def collect_form_data(self):
        """Collect form data into a dictionary for saving."""
        data = {
            "name": self.ui.lineEdit_9.text().strip(),
            "founding_date": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "number_of_members": safe_get_spinbox_value(self.ui.spinBox, 1),
            "main_activity": self.ui.lineEdit_11.text().strip(),
            "status": self.ui.lineEdit_10.text().strip() or "Active",
            "base_id": self.ui.comboBox_7.currentData()
        }
        
        return data
    
    def reset_form(self):
        """Reset form to default state."""
        self.ui.lineEdit_9.clear()  # Name field
        self.ui.lineEdit_11.clear()  # Main activity field
        self.ui.lineEdit_10.clear()  # Status field
        
        self.ui.spinBox.setValue(1)  # Number of members
        
        current_date = QDate.currentDate()
        self.ui.dateEdit.setDate(current_date)
        
        # Reset combobox if it has items
        if self.ui.comboBox_7.count() > 0:
            self.ui.comboBox_7.setCurrentIndex(0)