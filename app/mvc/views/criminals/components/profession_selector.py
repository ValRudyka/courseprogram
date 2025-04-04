from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QComboBox, QPushButton, QListWidget, QLabel)
from PySide6.QtCore import Signal

class ProfessionSelector(QWidget):
    selection_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.profession_ids = {} 
    def setup_ui(self):
        """Create the UI layout with combo box, add button and selection list."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        combo_layout = QHBoxLayout()
        self.profession_combo = QComboBox()
        self.profession_combo.setEditable(True)
        self.add_button = QPushButton("+")
        self.add_button.setMaximumWidth(30)
        combo_layout.addWidget(self.profession_combo)
        combo_layout.addWidget(self.add_button)
        
        self.selected_list = QListWidget()
        self.remove_button = QPushButton("Видалити")
        
        main_layout.addLayout(combo_layout)
        main_layout.addWidget(self.selected_list)
        main_layout.addWidget(self.remove_button)
        
        self.add_button.clicked.connect(self.add_profession)
        self.remove_button.clicked.connect(self.remove_profession)
    
    def load_professions(self, professions):
        """Load available professions into combo box."""
        self.profession_combo.clear()
        for profession in professions:
            self.profession_combo.addItem(profession["name"], profession["id"])
    
    def add_profession(self):
        """Add the currently selected profession to the list."""
        current_text = self.profession_combo.currentText()
        current_id = self.profession_combo.currentData()
        
        # Skip if already added or empty
        if not current_text or current_id in self.profession_ids:
            return
        
        # Add to list
        self.selected_list.addItem(current_text)
        self.profession_ids[current_id] = current_text
        self.selection_changed.emit()
    
    def remove_profession(self):
        """Remove the selected profession from the list."""
        selected_item = self.selected_list.currentItem()
        if not selected_item:
            return
            
        selected_text = selected_item.text()
        selected_id = None
        
        # Find ID by text
        for id, text in self.profession_ids.items():
            if text == selected_text:
                selected_id = id
                break
                
        if selected_id:
            del self.profession_ids[selected_id]
            self.selected_list.takeItem(self.selected_list.row(selected_item))
            self.selection_changed.emit()
    
    def get_selected_profession_ids(self):
        """Get list of selected profession IDs."""
        return list(self.profession_ids.keys())
    
    def set_selected_professions(self, professions):
        """Set preselected professions (for editing)."""
        self.clear_selection()
        
        for profession in professions:
            self.selected_list.addItem(profession["name"])
            self.profession_ids[profession["id"]] = profession["name"]
    
    def clear_selection(self):
        """Clear all selected professions."""
        self.selected_list.clear()
        self.profession_ids = {}