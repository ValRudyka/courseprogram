from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from .criminal_detail_source import Ui_MainWindow

class CriminalDetailView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Інформація про злочинця")
        
    def set_criminal_data(self, criminal_data):
        if not criminal_data:
            return
            
        self.ui.lineEdit.setText(criminal_data.get("first_name", ""))
        self.ui.lineEdit_2.setText(criminal_data.get("last_name", ""))
        self.ui.lineEdit_3.setText(criminal_data.get("nickname", ""))
        self.ui.lineEdit_4.setText(criminal_data.get("birth_place_name", ""))
        self.ui.lineEdit_5.setText(criminal_data.get("date_of_birth", ""))
        self.ui.lineEdit_6.setText(criminal_data.get("last_place_name", ""))
        self.ui.lineEdit_7.setText(criminal_data.get("group_name", ""))
        self.ui.lineEdit_8.setText(criminal_data.get("role", ""))
        
        self.ui.lineEdit_9.setText(str(criminal_data.get("height", "")))
        self.ui.lineEdit_10.setText(str(criminal_data.get("weight", "")))
        self.ui.lineEdit_11.setText(criminal_data.get("hair_color", ""))
        self.ui.lineEdit_12.setText(criminal_data.get("eye_color", ""))
        self.ui.lineEdit_13.setText(criminal_data.get("distinguishing_features", ""))
        
        self.ui.lineEdit_14.setText(criminal_data.get("last_case", ""))
        self.ui.lineEdit_15.setText(criminal_data.get("last_case_date", ""))
        self.ui.lineEdit_16.setText(criminal_data.get("last_case_location_name", ""))
        self.ui.lineEdit_17.setText(str(criminal_data.get("court_sentence", "")))
        self.ui.lineEdit_20.setText(criminal_data.get("crime_type", ""))  # Added this line
        
        languages = ", ".join([lang.get("name", "") for lang in criminal_data.get("languages", [])])
        professions = ", ".join([prof.get("name", "") for prof in criminal_data.get("professions", [])])
            
        self.ui.lineEdit_18.setText(languages)
        self.ui.lineEdit_19.setText(professions)