from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QComboBox, QLineEdit, QLabel)
from PySide6.QtCore import Signal

class GangSelector(QWidget):
    selection_changed = Signal()  

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Create the UI layout with combo box for single gang selection and role field."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        gang_layout = QHBoxLayout()
        self.label_gang = QLabel("Угруповання")
        self.gang_combo = QComboBox()
        gang_layout.addWidget(self.label_gang)
        gang_layout.addWidget(self.gang_combo)
        
        role_layout = QHBoxLayout()
        self.label_role = QLabel("Роль в угрупованні")
        self.role_edit = QLineEdit()
        role_layout.addWidget(self.label_role)
        role_layout.addWidget(self.role_edit)
        
        main_layout.addLayout(gang_layout)
        main_layout.addLayout(role_layout)

        self.gang_combo.currentIndexChanged.connect(self.on_selection_changed)
        self.role_edit.textChanged.connect(self.on_selection_changed)
    
    def load_gangs(self, gangs):
        """Load available criminal groups into combo box."""
        self.gang_combo.clear()
        self.gang_combo.addItem("Немає", None) 
        
        for gang in gangs:
            self.gang_combo.addItem(gang["name"], gang["id"])
    
    def on_selection_changed(self):
        """Handle changes in the selection."""
        self.selection_changed.emit()
    
    def get_selected_gang_id(self):
        """Get the selected gang ID."""
        return self.gang_combo.currentData()
    
    def get_role(self):
        """Get the role text."""
        return self.role_edit.text().strip()
    
    def set_selected_gang(self, gang_id, role=""):
        """Set preselected gang and role (for editing)."""
        index = self.gang_combo.findData(gang_id)
        if index >= 0:
            self.gang_combo.setCurrentIndex(index)
        else:
            self.gang_combo.setCurrentIndex(0) 
        
        self.role_edit.setText(role)
    
    def clear_selection(self):
        """Clear the gang selection."""
        self.gang_combo.setCurrentIndex(0) 
        self.role_edit.clear()