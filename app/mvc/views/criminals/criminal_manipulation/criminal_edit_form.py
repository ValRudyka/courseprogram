from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Signal, QDate, QRect
from .criminal_edit import Ui_MainWindow
from ..components.profession_selector import ProfessionSelector
from ..components.gang_selector import GangSelector
from ..components.language_selector import LanguageSelector
from utils.spinbox_utils import set_spinbox_with_data, safe_get_spinbox_value

class CriminalEditForm(QMainWindow):
    update_requested = Signal(int, dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setup_custom_components()
        
        self.setup_connections()
        
        self.criminal_id = None
    
    def setup_custom_components(self):
        """Replace standard combo boxes with custom components for many-to-many relationships."""
        self.profession_container = QWidget(self.ui.centralwidget)
        profession_layout = QVBoxLayout(self.profession_container)
        profession_layout.setContentsMargins(0, 0, 0, 0)
        
        self.profession_selector = ProfessionSelector()
        profession_layout.addWidget(self.profession_selector)
        
        orig_geom = self.ui.comboBox.geometry()
        expanded_geom = QRect(orig_geom.x(), orig_geom.y(), 
                            orig_geom.width(), orig_geom.height() * 5)
        self.profession_container.setGeometry(expanded_geom)
        
        self.ui.comboBox.hide()
        
        self.gang_container = QWidget(self.ui.centralwidget)
        gang_layout = QVBoxLayout(self.gang_container)
        gang_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gang_selector = GangSelector()
        gang_layout.addWidget(self.gang_selector)
        
        orig_geom = self.ui.comboBox_12.geometry()
        expanded_geom = QRect(orig_geom.x(), orig_geom.y(), 
                            orig_geom.width(), orig_geom.height() * 4) 
        self.gang_container.setGeometry(expanded_geom)
        
        self.ui.comboBox_12.hide()
        
        self.language_selector = LanguageSelector(self, use_internal_list=False)
        self.language_selector.language_list = self.ui.listWidget_2
        self.language_selector.language_list.itemSelectionChanged.connect(self.language_selector.on_selection_changed)
        self.ui.listWidget_2.clear()
    
    def setup_connections(self):
        """Connect UI elements to their corresponding actions."""
        self.ui.pushButton_2.clicked.connect(self.on_update)
    
    def load_reference_data(self, cities, professions, gangs, languages):
        """Load reference data into the form's selection elements."""
        self.ui.comboBox_8.clear() 
        self.ui.comboBox_9.clear()  
        self.ui.comboBox_10.clear()  
        self.language_selector.language_list.clear()
        self.language_selector.language_ids.clear()
        
        for city in cities:
            display_text = f"{city['name']}, {city['country']}"
            self.ui.comboBox_8.addItem(display_text, city['id'])
            self.ui.comboBox_9.addItem(display_text, city['id'])
            self.ui.comboBox_10.addItem(display_text, city['id'])
        
        self.profession_selector.load_professions(professions)
        self.gang_selector.load_gangs(gangs)
        self.ui.listWidget_2.clear()
    
        if languages:
            print(f"Loading {len(languages)} languages")
            self.language_selector.load_languages(languages)
        else:
            print("No languages data provided")
    
    def set_criminal_data(self, criminal_id, data):
        """Set form data for editing a criminal."""
        self.criminal_id = criminal_id
        
        self.ui.lineEdit_17.setText(data.get("first_name", ""))  
        self.ui.lineEdit_11.setText(data.get("last_name", ""))   
        self.ui.lineEdit_12.setText(data.get("nickname", ""))   
        self.ui.lineEdit_16.setText(data.get("distinguishing_features", ""))  
        self.ui.lineEdit_18.setText(data.get("last_case", ""))   
        
        self.gang_selector.set_selected_gang(data.get("id_group"), data.get("role", ""))

        set_spinbox_with_data(self.ui.spinBox_3, data, "height", default_value=170)
        set_spinbox_with_data(self.ui.spinBox_4, data, "weight", default_value=70)
        set_spinbox_with_data(self.ui.spinBox, data, "court_sentence", default_value=1)
        
        self.set_combobox_by_id(self.ui.comboBox_8, data.get("place_of_birth_id"))
        self.set_combobox_by_id(self.ui.comboBox_9, data.get("last_live_place_id"))
        self.set_combobox_by_id(self.ui.comboBox_10, data.get("last_case_location_id"))
        
        if data.get("eye_color"):
            index = self.ui.comboBox_4.findText(data.get("eye_color"))
            if index >= 0:
                self.ui.comboBox_4.setCurrentIndex(index)
        
        if data.get("hair_color"):
            index = self.ui.comboBox_3.findText(data.get("hair_color"))
            if index >= 0:
                self.ui.comboBox_3.setCurrentIndex(index)
        
        if data.get("birth_date"):
            birth_date = QDate.fromString(data.get("birth_date"), "yyyy-MM-dd")
            if birth_date.isValid():
                self.ui.dateEdit_4.setDate(birth_date)
        
        if data.get("last_case_date"):
            case_date = QDate.fromString(data.get("last_case_date"), "yyyy-MM-dd")
            if case_date.isValid():
                self.ui.dateEdit_3.setDate(case_date)
        
        if "professions" in data:
            self.profession_selector.set_selected_professions(data["professions"])
        
        if "languages" in data:
            print(f"Setting {len(data['languages'])} languages in criminal data")
            self.language_selector.set_selected_languages(data["languages"])
        else:
            print("No languages data in criminal record")
    
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
            
        if not self.validate_form():
            return
        
        data = self.collect_form_data()
        
        self.update_requested.emit(self.criminal_id, data)
    
    def validate_form(self):
        """Validate form input before updating."""
        if not self.ui.lineEdit_17.text().strip():
            QMessageBox.warning(self, "Validation Error", "Ім'я є обов'язковим")
            return False
            
        if not self.ui.lineEdit_11.text().strip(): 
            QMessageBox.warning(self, "Validation Error", "Прізвище є обов'язковим")
            return False
        
        return True
    
    def collect_form_data(self):
        """Collect form data into a dictionary for updating."""
        data = {
            "first_name": self.ui.lineEdit_17.text().strip(),
            "last_name": self.ui.lineEdit_11.text().strip(),
            "nickname": self.ui.lineEdit_12.text().strip(),
            "birth_place_id": self.ui.comboBox_8.currentData(),
            "birth_date": self.ui.dateEdit_4.date().toString("yyyy-MM-dd"),
            "last_residence_id": self.ui.comboBox_9.currentData(),
            "height": safe_get_spinbox_value(self.ui.spinBox_3, 170),
            "weight": safe_get_spinbox_value(self.ui.spinBox_4, 70),
            "eye_color": self.ui.comboBox_4.currentText(),
            "hair_color": self.ui.comboBox_3.currentText(),
            "distinguishing_features": self.ui.lineEdit_16.text().strip(),
            "last_case": self.ui.lineEdit_18.text().strip(),
            "last_case_date": self.ui.dateEdit_3.date().toString("yyyy-MM-dd"),
            "last_case_location_id": self.ui.comboBox_10.currentData(),
            "id_group": self.gang_selector.get_selected_gang_id(),
            "role": self.gang_selector.get_role(),
            "profession_ids": self.profession_selector.get_selected_profession_ids(),
            "language_ids": self.language_selector.get_selected_language_ids(),
            "court_sentence": safe_get_spinbox_value(self.ui.spinBox, 1) 
        }
        
        return data