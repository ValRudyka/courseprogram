from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt
from .filter_header_view import FilterHeaderView
from .criminal_filter_model import CriminalFilterProxyModel

class FilterableTableView(QTableView):
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
        self.filter_model = CriminalFilterProxyModel(self)
        self.filter_model.setSourceModel(model)
        
        super().setModel(self.filter_model)
        
        self.filter_header.setModel(model)
        
    def applyFilter(self, column, text):
        if not self.filter_model:
            return
            
        self.filter_model.setColumnFilter(column, text)
        
    def clearFilters(self):
        if hasattr(self, 'filter_header') and self.filter_header and hasattr(self.filter_header, 'clearFilters'):
            self.filter_header.clearFilters()
        
        if self.filter_model and hasattr(self.filter_model, 'clearFilters'):
            self.filter_model.clearFilters()
        
    def sourceModel(self):
        if self.filter_model:
            return self.filter_model.sourceModel()
        return self.model()
        
    def setFilterVisible(self, visible):
        if hasattr(self, 'filter_header') and self.filter_header:
            self.filter_header.setFilterVisible(visible)