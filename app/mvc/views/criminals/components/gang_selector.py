from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox
from PySide6.QtCore import Signal

class GangSelector(QWidget):
    selection_changed = Signal()  

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Create the UI layout with just an editable combo box for gang selection."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gang_combo = QComboBox()
        self.gang_combo.setEditable(True)
        main_layout.addWidget(self.gang_combo)

        self.gang_combo.currentIndexChanged.connect(self.on_selection_changed)
        self.gang_combo.editTextChanged.connect(self.on_selection_changed)
    
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
    
    def set_selected_gang(self, gang_id, role=""):
        """Set preselected gang (for editing)."""
        index = self.gang_combo.findData(gang_id)
        if index >= 0:
            self.gang_combo.setCurrentIndex(index)
        else:
            self.gang_combo.setCurrentIndex(0) 
    
    def clear_selection(self):
        """Clear the gang selection."""
        self.gang_combo.setCurrentIndex(0)