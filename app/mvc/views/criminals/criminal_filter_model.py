from PySide6.QtCore import QSortFilterProxyModel, Qt, QDate

class CriminalFilterProxyModel(QSortFilterProxyModel):
    """
    Enhanced filter proxy model for criminal data.
    
    Provides column-specific filtering capabilities, including:
    - Different comparison modes for date fields
    - Numeric range filtering for height/weight
    - Case-insensitive text filtering
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
                
            # Convert to string for comparison
            data_str = str(data).lower()
            filter_text = filter_text.lower()
            
            # Check for special column handling
            # ID column (exact match or contains)
            if column == 0:  # ID column
                if filter_text not in data_str:
                    return False
                    
            # Date column (date comparison)
            elif column == 4:  # Birth date column
                # Skip if data is not a date
                if not data_str:
                    return False
                    
                # Simple contains for now (could be enhanced with date comparison)
                if filter_text not in data_str:
                    return False
                    
            # Height and Weight columns (numeric range)
            elif column in [7, 8]:  # Height/Weight columns
                # Remove units and convert to numeric
                try:
                    if column == 7:  # Height
                        value = int(data_str.replace('см', '').strip())
                    else:  # Weight
                        value = int(data_str.replace('кг', '').strip())
                        
                    # Handle ranges like "160-180" or inequalities like ">160"
                    if '-' in filter_text:
                        # Range filter
                        min_val, max_val = filter_text.split('-')
                        min_val = int(min_val.strip()) if min_val.strip() else 0
                        max_val = int(max_val.strip()) if max_val.strip() else float('inf')
                        
                        if not (min_val <= value <= max_val):
                            return False
                    elif filter_text.startswith('>'):
                        # Greater than
                        min_val = int(filter_text[1:].strip())
                        if value <= min_val:
                            return False
                    elif filter_text.startswith('<'):
                        # Less than
                        max_val = int(filter_text[1:].strip())
                        if value >= max_val:
                            return False
                    elif filter_text.isdigit():
                        # Exact match
                        if value != int(filter_text):
                            return False
                    else:
                        # Simple contains
                        if filter_text not in data_str:
                            return False
                except (ValueError, TypeError):
                    # If conversion fails, do simple contains
                    if filter_text not in data_str:
                        return False
            else:
                # Default filtering: case-insensitive contains
                if filter_text not in data_str:
                    return False
                    
        # All filters passed
        return True