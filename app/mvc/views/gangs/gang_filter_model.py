from PySide6.QtCore import QSortFilterProxyModel, Qt, QDate

class GangFilterProxyModel(QSortFilterProxyModel):
    """
    Provides column-specific filtering capabilities for gang table, including:
    - Date filtering for founding date
    - Numeric range filtering for member counts
    - Case-insensitive text filtering for names and activities
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        self.column_filters = {}
        
    def setColumnFilter(self, column, text):
        """Set filter text for a specific column."""
        if not text:
            if column in self.column_filters:
                del self.column_filters[column]
        else:
            self.column_filters[column] = text
            
        self.invalidateFilter()
        
    def clearFilters(self):
        """Clear all filters."""
        self.column_filters.clear()
        self.invalidateFilter()
        
    def filterAcceptsRow(self, source_row, source_parent):
        """Determine if a row should be shown based on all column filters."""
        if not self.column_filters:
            return True
            
        for column, filter_text in self.column_filters.items():
            if not filter_text:
                continue
                
            index = self.sourceModel().index(source_row, column, source_parent)
            data = self.sourceModel().data(index, Qt.DisplayRole)
            
            if data is None:
                return False
                
            data_str = str(data).lower()
            filter_text = filter_text.lower()
            
            if column in [0, 1, 4, 5]:
                if filter_text not in data_str:
                    return False
            
            elif column == 2:
                if not data_str:
                    return False
                
                if filter_text.startswith('>'):
                    filter_date = filter_text[1:].strip()
                    if data_str <= filter_date:
                        return False
                elif filter_text.startswith('<'):
                    filter_date = filter_text[1:].strip()
                    if data_str >= filter_date:
                        return False
                elif '-' in filter_text:
                    start_date, end_date = filter_text.split('-')
                    if not (start_date.strip() <= data_str <= end_date.strip()):
                        return False
                elif filter_text not in data_str:
                    return False
                
            elif column in [3, 6]:
                try:
                    value = int(data_str)
                    
                    if '-' in filter_text:
                        min_val, max_val = filter_text.split('-')
                        min_val = int(min_val.strip()) if min_val.strip() else 0
                        max_val = int(max_val.strip()) if max_val.strip() else float('inf')
                        
                        if not (min_val <= value <= max_val):
                            return False
                    elif filter_text.startswith('>'):
                        min_val = int(filter_text[1:].strip())
                        if value <= min_val:
                            return False
                    elif filter_text.startswith('<'):
                        max_val = int(filter_text[1:].strip())
                        if value >= max_val:
                            return False
                    elif filter_text.isdigit():
                        if value != int(filter_text):
                            return False
                    else:
                        if filter_text not in data_str:
                            return False
                except (ValueError, TypeError):
                    if filter_text not in data_str:
                        return False
                        
        return True