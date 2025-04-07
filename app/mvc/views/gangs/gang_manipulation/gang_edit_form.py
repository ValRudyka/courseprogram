from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal, QDate
from .gang_edit import Ui_MainWindow
from utils.spinbox_utils import safe_get_spinbox_value, safe_set_spinbox_value

class GangEditForm(QMainWindow):
    update_requested = Signal(int, dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setup_connections()
        
        self.gang_id = None
    
    def setup_connections(self):
        """Connect UI elements to their corresponding actions."""
        self.ui.pushButton_2.clicked.connect(self.on_update)
    
    def load_reference_data(self, cities):
        """Load city data for location selection."""
        self.ui.comboBox.clear()
        
        for city in cities:
            display_text = f"{city['name']}, {city['country']}"
            self.ui.comboBox.addItem(display_text, city['id'])
    
    def set_gang_data(self, gang_id, data):
        """Set form data for editing a gang."""
        self.gang_id = gang_id
        
        self.ui.lineEdit.setText(data.get("name", ""))  
        self.ui.lineEdit_2.setText(data.get("main_activity", ""))  
        self.ui.lineEdit_3.setText(data.get("status", ""))  
        
        safe_set_spinbox_value(self.ui.spinBox, data.get("number_of_members"), 1)
        
        # Set founding date
        if data.get("founding_date"):
            founding_date = QDate.fromString(data.get("founding_date"), "yyyy-MM-dd")
            if founding_date.isValid():
                self.ui.dateEdit.setDate(founding_date)
        
        # Set base location
        self.set_combobox_by_id(self.ui.comboBox, data.get("base_id"))
    
    def set_combobox_by_id(self, combobox, item_id):
        """Set the selected item in a combo box by its data ID."""
        if item_id is None:
            return
            
        for i in range(combobox.count()):
            if combobox.itemData(i) == item_id:
                combobox.setCurrentIndex(i)
                break
    
    def on_update(self):
        """Handle update button click."""
        if self.gang_id is None:
            QMessageBox.warning(self, "Помилка", "Не вибрано угруповання для редагування")
            return
            
        if not self.validate_form():
            return
        
        data = self.collect_form_data()
        
        self.update_requested.emit(self.gang_id, data)
    
    def validate_form(self):
        """Validate form input before updating."""
        if not self.ui.lineEdit.text().strip():
            QMessageBox.warning(self, "Помилка валідації", "Назва є обов'язковою")
            return False
        
        return True
    
    def collect_form_data(self):
        """Collect form data into a dictionary for updating."""
        data = {
            "name": self.ui.lineEdit.text().strip(),
            "founding_date": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "number_of_members": safe_get_spinbox_value(self.ui.spinBox, 1),
            "main_activity": self.ui.lineEdit_2.text().strip(),
            "status": self.ui.lineEdit_3.text().strip() or "Active",
            "base_id": self.ui.comboBox.currentData()
        }
        
        return data