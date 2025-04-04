from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QComboBox, QPushButton, QListWidget, QLabel)
from PySide6.QtCore import Signal

class GangSelector(QWidget):
    selection_changed = Signal()  

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.gang_ids = {}  
        
    def setup_ui(self):
        """Create the UI layout with combo box, add button and selection list."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        combo_layout = QHBoxLayout()
        self.gang_combo = QComboBox()
        self.gang_combo.setEditable(True)
        self.add_button = QPushButton("+")
        self.add_button.setMaximumWidth(30)
        combo_layout.addWidget(self.gang_combo)
        combo_layout.addWidget(self.add_button)
        
        # List to display selected gangs
        self.selected_list = QListWidget()
        self.remove_button = QPushButton("Видалити")
        
        # Add widgets to layout
        main_layout.addLayout(combo_layout)
        main_layout.addWidget(self.selected_list)
        main_layout.addWidget(self.remove_button)
        
        # Connect signals
        self.add_button.clicked.connect(self.add_gang)
        self.remove_button.clicked.connect(self.remove_gang)
    
    def load_gangs(self, gangs):
        """Load available criminal groups into combo box."""
        self.gang_combo.clear()
        for gang in gangs:
            self.gang_combo.addItem(gang["name"], gang["id"])
    
    def add_gang(self):
        """Add the currently selected gang to the list."""
        current_text = self.gang_combo.currentText()
        current_id = self.gang_combo.currentData()
        
        if not current_text or current_id in self.gang_ids:
            return
        
        self.selected_list.addItem(current_text)
        self.gang_ids[current_id] = current_text
        self.selection_changed.emit()
    
    def remove_gang(self):
        """Remove the selected gang from the list."""
        selected_item = self.selected_list.currentItem()
        if not selected_item:
            return
            
        selected_text = selected_item.text()
        selected_id = None
        
        for id, text in self.gang_ids.items():
            if text == selected_text:
                selected_id = id
                break
                
        if selected_id:
            del self.gang_ids[selected_id]
            self.selected_list.takeItem(self.selected_list.row(selected_item))
            self.selection_changed.emit()
    
    def get_selected_gang_ids(self):
        """Get list of selected gang IDs."""
        return list(self.gang_ids.keys())
    
    def set_selected_gangs(self, gangs):
        """Set preselected gangs (for editing)."""
        self.clear_selection()
        
        for gang in gangs:
            self.selected_list.addItem(gang["name"])
            self.gang_ids[gang["id"]] = gang["name"]
    
    def clear_selection(self):
        """Clear all selected gangs."""
        self.selected_list.clear()
        self.gang_ids = {}