from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Signal, QDate
from .criminal_add import Ui_MainWindow
from ..components.profession_selector import ProfessionSelector
from ..components.gang_selector import GangSelector
from ..components.language_selector import LanguageSelector
from utils.spinbox_utils import safe_set_spinbox_value, safe_get_spinbox_value

class CriminalAddForm(QMainWindow):
    save_requested = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setup_custom_components()
        self.setup_connections()
        self.reset_form()
    
    def setup_custom_components(self):
        """Replace standard combo boxes with custom components for many-to-many relationships."""
        self.profession_container = QWidget()
        profession_layout = QVBoxLayout(self.profession_container)
        profession_layout.setContentsMargins(0, 0, 0, 0)
        
        self.profession_selector = ProfessionSelector()
        profession_layout.addWidget(self.profession_selector)
        
        parent_layout = self.ui.comboBox_13.parentWidget().layout()
        if parent_layout:
            parent_layout.replaceWidget(self.ui.comboBox_13, self.profession_container)
            self.ui.comboBox_13.hide()
        
        self.gang_container = QWidget()
        gang_layout = QVBoxLayout(self.gang_container)
        gang_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gang_selector = GangSelector()
        gang_layout.addWidget(self.gang_selector)
        
        parent_layout = self.ui.comboBox_11.parentWidget().layout()
        if parent_layout:
            parent_layout.replaceWidget(self.ui.comboBox_11, self.gang_container)
            self.ui.comboBox_11.hide()
            
        self.language_container = QWidget()

        
        self.language_selector = LanguageSelector(self)
    
        self.language_selector.language_list = self.ui.listWidget
        self.ui.listWidget.clear()
    
    def setup_connections(self):
        """Connect UI elements to their corresponding actions."""
        self.ui.pushButton.clicked.connect(self.on_save)
    
    def load_reference_data(self, cities, professions, gangs, languages):
        self.ui.comboBox_5.clear()  
        self.ui.comboBox_6.clear()  
        self.ui.comboBox_7.clear()  
        
        for city in cities:
            display_text = f"{city['name']}, {city['country']}"
            self.ui.comboBox_5.addItem(display_text, city['id'])
            self.ui.comboBox_6.addItem(display_text, city['id'])
            self.ui.comboBox_7.addItem(display_text, city['id'])
        
        self.profession_selector.load_professions(professions)
        self.gang_selector.load_gangs(gangs)
        self.ui.listWidget.clear()
    
        if languages:
            print(f"Loading {len(languages)} languages")
            self.language_selector.load_languages(languages)
        else:
            print("No languages data provided")
    
    def on_save(self):
        """Handle save button click."""
        if not self.validate_form():
            return
        
        data = self.collect_form_data()
        
        self.save_requested.emit(data)
    
    def validate_form(self):
        """Validate form input before saving."""
        if not self.ui.lineEdit_3.text().strip(): 
            QMessageBox.warning(self, "Validation Error", "Ім'я є обов'язковим")
            return False
            
        if not self.ui.lineEdit_4.text().strip():
            QMessageBox.warning(self, "Validation Error", "Прізвище є обов'язковим")
            return False
        
        return True
    
    def collect_form_data(self):
        """Collect form data into a dictionary for saving."""
        data = {
            "first_name": self.ui.lineEdit_3.text().strip(),
            "last_name": self.ui.lineEdit_4.text().strip(),
            "nickname": self.ui.lineEdit_5.text().strip(),
            "birth_place_id": self.ui.comboBox_5.currentData(),
            "birth_date": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "last_residence_id": self.ui.comboBox_6.currentData(),
            "height": safe_get_spinbox_value(self.ui.spinBox, 170),
            "weight": safe_get_spinbox_value(self.ui.spinBox_2, 70),
            "eye_color": self.ui.comboBox.currentText(),
            "hair_color": self.ui.comboBox_2.currentText(),
            "distinguishing_features": self.ui.lineEdit_6.text().strip(),
            "last_case": self.ui.lineEdit_8.text().strip(),
            "last_case_date": self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),
            "last_case_location_id": self.ui.comboBox_7.currentData(),
            "id_group": self.gang_selector.get_selected_gang_id(),
            "role": self.gang_selector.get_role(),
            "profession_ids": self.profession_selector.get_selected_profession_ids(),
            "language_ids": self.language_selector.get_selected_language_ids(),
            "court_sentence": safe_get_spinbox_value(self.ui.spinBox_3, 1) 
        }
        
        return data
    
    def reset_form(self):
        """Reset form to default state."""
        self.ui.lineEdit_3.clear()  
        self.ui.lineEdit_4.clear()  
        self.ui.lineEdit_5.clear()  
        self.ui.lineEdit_6.clear()  
        self.ui.lineEdit_8.clear() 
        
        safe_set_spinbox_value(self.ui.spinBox, 170)
        safe_set_spinbox_value(self.ui.spinBox_2, 70)
        safe_set_spinbox_value(self.ui.spinBox_3, 1) 
        
        current_date = QDate.currentDate()
        self.ui.dateEdit.setDate(current_date)
        self.ui.dateEdit_2.setDate(current_date)
        
        self.profession_selector.clear_selection()
        self.gang_selector.clear_selection()
        self.language_selector.clear_selection()
        
        if self.ui.comboBox.count() > 0:
            self.ui.comboBox.setCurrentIndex(0)
        if self.ui.comboBox_2.count() > 0:
            self.ui.comboBox_2.setCurrentIndex(0)