from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Signal, QDate
from .criminal_edit import Ui_MainWindow
from ..components.profession_selector import ProfessionSelector
from ..components.gang_selector import GangSelector

class CriminalEditForm(QMainWindow):
    update_requested = Signal(int, dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Set up custom components
        self.setup_custom_components()
        
        # Connect signals
        self.setup_connections()
        
        # Criminal ID for the record being edited
        self.criminal_id = None
        
        # Language name to ID mapping
        self.language_map = {}
    
    def setup_custom_components(self):
        """Replace standard combo boxes with custom components for many-to-many relationships."""
        # Replace profession combo box with custom component
        self.profession_container = QWidget()
        profession_layout = QVBoxLayout(self.profession_container)
        profession_layout.setContentsMargins(0, 0, 0, 0)
        
        self.profession_selector = ProfessionSelector()
        profession_layout.addWidget(self.profession_selector)
        
        # Get the parent layout of comboBox and replace it
        parent_layout = self.ui.comboBox.parentWidget().layout()
        if parent_layout:
            parent_layout.replaceWidget(self.ui.comboBox, self.profession_container)
            self.ui.comboBox.hide()
        
        # Replace gang combo box with custom component
        self.gang_container = QWidget()
        gang_layout = QVBoxLayout(self.gang_container)
        gang_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gang_selector = GangSelector()
        gang_layout.addWidget(self.gang_selector)
        
        # Get the parent layout of comboBox_12 and replace it
        parent_layout = self.ui.comboBox_12.parentWidget().layout()
        if parent_layout:
            parent_layout.replaceWidget(self.ui.comboBox_12, self.gang_container)
            self.ui.comboBox_12.hide()
    
    def setup_connections(self):
        """Connect UI elements to their corresponding actions."""
        # Connect the update button
        self.ui.pushButton_2.clicked.connect(self.on_update)
    
    def load_reference_data(self, cities, professions, gangs, languages):
        """Load reference data into the form's selection elements."""
        # Clear existing items
        self.ui.comboBox_8.clear()  # Birth place
        self.ui.comboBox_9.clear()  # Last residence
        self.ui.comboBox_10.clear()  # Last case location
        
        # Add cities to combo boxes with display text and ID as data
        for city in cities:
            display_text = f"{city['name']}, {city['country']}"
            self.ui.comboBox_8.addItem(display_text, city['id'])
            self.ui.comboBox_9.addItem(display_text, city['id'])
            self.ui.comboBox_10.addItem(display_text, city['id'])
        
        # Load professions and gangs into custom selectors
        self.profession_selector.load_professions(professions)
        self.gang_selector.load_gangs(gangs)
        
        # For languages, we can use the existing QListWidget
        # but we need to map language names to IDs
        self.language_map = {lang['name']: lang['id'] for lang in languages}
    
    def set_criminal_data(self, criminal_id, data):
        """Set form data for editing a criminal."""
        self.criminal_id = criminal_id
        
        # Set text fields
        self.ui.lineEdit_17.setText(data.get("first_name", ""))  # First name
        self.ui.lineEdit_11.setText(data.get("last_name", ""))   # Last name
        self.ui.lineEdit_12.setText(data.get("nickname", ""))    # Nickname
        self.ui.lineEdit_16.setText(data.get("distinguishing_features", ""))  # Features
        self.ui.lineEdit_18.setText(data.get("last_case", ""))   # Last case
        
        # Set numeric fields
        self.ui.spinBox_3.setValue(data.get("height", 170))
        self.ui.spinBox_4.setValue(data.get("weight", 70))
        
        # Set combo box selections
        self.set_combobox_by_id(self.ui.comboBox_8, data.get("place_of_birth_id"))
        self.set_combobox_by_id(self.ui.comboBox_9, data.get("last_live_place_id"))
        self.set_combobox_by_id(self.ui.comboBox_10, data.get("last_case_location_id"))
        
        # Set eye and hair color
        if data.get("eye_color"):
            index = self.ui.comboBox_4.findText(data.get("eye_color"))
            if index >= 0:
                self.ui.comboBox_4.setCurrentIndex(index)
        
        if data.get("hair_color"):
            index = self.ui.comboBox_3.findText(data.get("hair_color"))
            if index >= 0:
                self.ui.comboBox_3.setCurrentIndex(index)
        
        # Set dates
        if data.get("birth_date"):
            birth_date = QDate.fromString(data.get("birth_date"), "yyyy-MM-dd")
            if birth_date.isValid():
                self.ui.dateEdit_4.setDate(birth_date)
        
        if data.get("last_case_date"):
            case_date = QDate.fromString(data.get("last_case_date"), "yyyy-MM-dd")
            if case_date.isValid():
                self.ui.dateEdit_3.setDate(case_date)
        
        # Set many-to-many relationships
        if "professions" in data:
            self.profession_selector.set_selected_professions(data["professions"])
        
        if "groups" in data:
            self.gang_selector.set_selected_gangs(data["groups"])
        
        # Set language selections
        if "languages" in data:
            for i in range(self.ui.listWidget_2.count()):
                item = self.ui.listWidget_2.item(i)
                for lang in data["languages"]:
                    if item.text() == lang.get("name"):
                        item.setSelected(True)
                        break
    
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
        if self.criminal_id is None:
            QMessageBox.warning(self, "Error", "No criminal selected for editing")
            return
            
        # Validate form
        if not self.validate_form():
            return
        
        # Collect form data
        data = self.collect_form_data()
        
        # Emit signal with criminal ID and collected data
        self.update_requested.emit(self.criminal_id, data)
    
    def validate_form(self):
        """Validate form input before updating."""
        if not self.ui.lineEdit_17.text().strip():  # First name
            QMessageBox.warning(self, "Validation Error", "Ім'я є обов'язковим")
            return False
            
        if not self.ui.lineEdit_11.text().strip():  # Last name
            QMessageBox.warning(self, "Validation Error", "Прізвище є обов'язковим")
            return False
        
        return True
    
    def collect_form_data(self):
        """Collect form data into a dictionary for updating."""
        # Get selected language IDs
        language_ids = []
        for i in range(self.ui.listWidget_2.count()):
            item = self.ui.listWidget_2.item(i)
            if item.isSelected():
                language_name = item.text()
                if language_name in self.language_map:
                    language_ids.append(self.language_map[language_name])
        
        # Collect all form data
        data = {
            "first_name": self.ui.lineEdit_17.text().strip(),
            "last_name": self.ui.lineEdit_11.text().strip(),
            "nickname": self.ui.lineEdit_12.text().strip(),
            "birth_place_id": self.ui.comboBox_8.currentData(),
            "birth_date": self.ui.dateEdit_4.date().toString("yyyy-MM-dd"),
            "last_residence_id": self.ui.comboBox_9.currentData(),
            "height": self.ui.spinBox_3.value(),
            "weight": self.ui.spinBox_4.value(),
            "eye_color": self.ui.comboBox_4.currentText(),
            "hair_color": self.ui.comboBox_3.currentText(),
            "distinguishing_features": self.ui.lineEdit_16.text().strip(),
            "last_case": self.ui.lineEdit_18.text().strip(),
            "last_case_date": self.ui.dateEdit_3.date().toString("yyyy-MM-dd"),
            "last_case_location_id": self.ui.comboBox_10.currentData(),
            # Many-to-many relationships
            "profession_ids": self.profession_selector.get_selected_profession_ids(),
            "group_ids": self.gang_selector.get_selected_gang_ids(),
            "language_ids": language_ids
        }
        
        return data