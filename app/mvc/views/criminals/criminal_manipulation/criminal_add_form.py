from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QAbstractItemView
from PySide6.QtCore import Signal, QDate
from .criminal_add import Ui_MainWindow
from ..components.profession_selector import ProfessionSelector
from ..components.gang_selector import GangSelector

class CriminalAddForm(QMainWindow):
    save_requested = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setup_custom_components()
        self.setup_connections()
        self.reset_form()
        
        self.language_map = {}
    
    def setup_custom_components(self):
        """Replace standard combo boxes with custom components for many-to-many relationships."""
        # Replace profession combo box with custom component
        self.profession_container = QWidget()
        profession_layout = QVBoxLayout(self.profession_container)
        profession_layout.setContentsMargins(0, 0, 0, 0)
        
        self.profession_selector = ProfessionSelector()
        profession_layout.addWidget(self.profession_selector)
        
        # Get the parent layout of comboBox_13 and replace it
        parent_layout = self.ui.comboBox_13.parentWidget().layout()
        if parent_layout:
            parent_layout.replaceWidget(self.ui.comboBox_13, self.profession_container)
            self.ui.comboBox_13.hide()
        
        # Replace gang combo box with custom component
        self.gang_container = QWidget()
        gang_layout = QVBoxLayout(self.gang_container)
        gang_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gang_selector = GangSelector()
        gang_layout.addWidget(self.gang_selector)
        
        # Get the parent layout of comboBox_11 and replace it
        parent_layout = self.ui.comboBox_11.parentWidget().layout()
        if parent_layout:
            parent_layout.replaceWidget(self.ui.comboBox_11, self.gang_container)
            self.ui.comboBox_11.hide()
    
    def setup_connections(self):
        """Connect UI elements to their corresponding actions."""
        # Connect the add button
        self.ui.pushButton.clicked.connect(self.on_save)
    
    def load_reference_data(self, cities, professions, gangs, languages):
        """Load reference data into the form's selection elements."""
        # Clear existing items
        self.ui.comboBox_5.clear()  # Birth place
        self.ui.comboBox_6.clear()  # Last residence
        self.ui.comboBox_7.clear()  # Last case location
        
        # Add cities to combo boxes with display text and ID as data
        for city in cities:
            display_text = f"{city['name']}, {city['country']}"
            self.ui.comboBox_5.addItem(display_text, city['id'])
            self.ui.comboBox_6.addItem(display_text, city['id'])
            self.ui.comboBox_7.addItem(display_text, city['id'])
        
        # Load professions and gangs into custom selectors
        self.profession_selector.load_professions(professions)
        self.gang_selector.load_gangs(gangs)
        
        # For languages, we can use the existing QListWidget
        # but we need to map language names to IDs
        self.language_map = {lang['name']: lang['id'] for lang in languages}
    
    def on_save(self):
        """Handle save button click."""
        # Validate form
        if not self.validate_form():
            return
        
        # Collect form data
        data = self.collect_form_data()
        
        # Emit signal with collected data
        self.save_requested.emit(data)
    
    def validate_form(self):
        """Validate form input before saving."""
        # Check required fields
        if not self.ui.lineEdit_3.text().strip():  # First name
            QMessageBox.warning(self, "Validation Error", "Ім'я є обов'язковим")
            return False
            
        if not self.ui.lineEdit_4.text().strip():  # Last name
            QMessageBox.warning(self, "Validation Error", "Прізвище є обов'язковим")
            return False
        
        # More validation as needed
        
        return True
    
    def collect_form_data(self):
        """Collect form data into a dictionary for saving."""
        # Get selected language IDs
        language_ids = []
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            if item.isSelected():
                language_name = item.text()
                if language_name in self.language_map:
                    language_ids.append(self.language_map[language_name])
        
        # Collect all form data
        data = {
            "first_name": self.ui.lineEdit_3.text().strip(),
            "last_name": self.ui.lineEdit_4.text().strip(),
            "nickname": self.ui.lineEdit_5.text().strip(),
            "birth_place_id": self.ui.comboBox_5.currentData(),
            "birth_date": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "last_residence_id": self.ui.comboBox_6.currentData(),
            "height": self.ui.spinBox.value(),
            "weight": self.ui.spinBox_2.value(),
            "eye_color": self.ui.comboBox.currentText(),
            "hair_color": self.ui.comboBox_2.currentText(),
            "distinguishing_features": self.ui.lineEdit_6.text().strip(),
            "last_case": self.ui.lineEdit_8.text().strip(),
            "last_case_date": self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),
            "last_case_location_id": self.ui.comboBox_7.currentData(),
            # Many-to-many relationships
            "profession_ids": self.profession_selector.get_selected_profession_ids(),
            "group_ids": self.gang_selector.get_selected_gang_ids(),
            "language_ids": language_ids
        }
        
        return data
    
    def reset_form(self):
        """Reset form to default state."""
        # Clear text fields
        self.ui.lineEdit_3.clear()  # First name
        self.ui.lineEdit_4.clear()  # Last name
        self.ui.lineEdit_5.clear()  # Nickname
        self.ui.lineEdit_6.clear()  # Distinguishing features
        self.ui.lineEdit_8.clear()  # Last case
        
        # Set default values for spinners
        self.ui.spinBox.setValue(170)  # Default height
        self.ui.spinBox_2.setValue(70)  # Default weight
        
        current_date = QDate.currentDate()
        self.ui.dateEdit.setDate(current_date)
        self.ui.dateEdit_2.setDate(current_date)
        
        # Clear selections
        self.profession_selector.clear_selection()
        self.gang_selector.clear_selection()
        
        # Clear language selections
        for i in range(self.ui.listWidget.count()):
            self.ui.listWidget.item(i).setSelected(False)
        
        # Reset combo box selections to first item if available
        if self.ui.comboBox.count() > 0:
            self.ui.comboBox.setCurrentIndex(0)
        if self.ui.comboBox_2.count() > 0:
            self.ui.comboBox_2.setCurrentIndex(0)