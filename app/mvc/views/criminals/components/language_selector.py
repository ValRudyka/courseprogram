from PySide6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QLabel,
                              QAbstractItemView)
from PySide6.QtCore import Signal

class LanguageSelector(QWidget):
    selection_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.language_ids = {}
    
    def setup_ui(self):
        """Create the UI layout with a list widget for multiple selection."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label for the list
        self.label = QLabel("Знання мов")
        main_layout.addWidget(self.label)
        
        self.language_list = QListWidget()
        self.language_list.setSelectionMode(QAbstractItemView.MultiSelection)
        main_layout.addWidget(self.language_list)
        
        # Connect signals
        self.language_list.itemSelectionChanged.connect(self.on_selection_changed)
    
    def load_languages(self, languages):
        """Load available languages into the list widget."""
        # Ensure we start with a clean slate
        self.language_list.clear()
        self.language_ids = {}
        
        # Add languages from database
        for language in languages:
            self.language_list.addItem(language["name"])
            self.language_ids[language["name"]] = language["id"]
    
    def on_selection_changed(self):
        """Handle changes in the selection."""
        self.selection_changed.emit()
    
    def get_selected_language_ids(self):
        """Get list of selected language IDs."""
        selected_ids = []
        for i in range(self.language_list.count()):
            item = self.language_list.item(i)
            if item.isSelected():
                language_name = item.text()
                if language_name in self.language_ids:
                    selected_ids.append(self.language_ids[language_name])
        return selected_ids
    
    def set_selected_languages(self, languages):
        """Set preselected languages (for editing)."""
        self.clear_selection()
        
        language_names = {lang["name"] for lang in languages}
        
        for i in range(self.language_list.count()):
            item = self.language_list.item(i)
            if item.text() in language_names:
                item.setSelected(True)
    
    def clear_selection(self):
        """Clear all selected languages."""
        for i in range(self.language_list.count()):
            self.language_list.item(i).setSelected(False)