from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt
from .filter_header_view import FilterHeaderView
from .criminal_filter_model import CriminalFilterProxyModel

class FilterableTableView(QTableView):
    """
    A table view with filter inputs in the header.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.filter_model = None
        
        self.filter_header = FilterHeaderView(Qt.Horizontal, self)
        self.setHorizontalHeader(self.filter_header)
        
        self.filter_header.filterChanged.connect(self.applyFilter)
        
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)
        
    def setModel(self, model):
        """Override to insert a proxy model for filtering."""
        # Create our custom filter proxy model
        self.filter_model = CriminalFilterProxyModel(self)
        self.filter_model.setSourceModel(model)
        
        # Set the proxy model instead of the original
        super().setModel(self.filter_model)
        
        # Update the header with the model
        self.filter_header.setModel(model)
        
    def applyFilter(self, column, text):
        """Apply a filter on a specific column."""
        if not self.filter_model:
            return
            
        # Apply column-specific filter
        self.filter_model.setColumnFilter(column, text)
        
    def clearFilters(self):
        """Clear all filters."""
        if hasattr(self, 'filter_header') and self.filter_header and hasattr(self.filter_header, 'clearFilters'):
            self.filter_header.clearFilters()
        
        if self.filter_model and hasattr(self.filter_model, 'clearFilters'):
            self.filter_model.clearFilters()
        
    def sourceModel(self):
        """Get the original source model."""
        if self.filter_model:
            return self.filter_model.sourceModel()
        return self.model()
        
    def setFilterVisible(self, visible):
        """Show or hide the filter row."""
        if hasattr(self, 'filter_header') and self.filter_header:
            self.filter_header.setFilterVisible(visible)