from PySide6.QtCore import QSortFilterProxyModel, Qt, QDate

class CriminalFilterProxyModel(QSortFilterProxyModel):
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
            
            if column == 4: 
                if not data_str:
                    return False
                    
                if '-' in filter_text and not filter_text.startswith('>') and not filter_text.startswith('<'):
                    try:
                        start_date, end_date = filter_text.split('-')
                        start_date = start_date.strip()
                        end_date = end_date.strip()
                        
                        if start_date and end_date:
                            if not (start_date <= data_str <= end_date):
                                return False
                        elif start_date:
                            if data_str < start_date:
                                return False
                        elif end_date:
                            if data_str > end_date:
                                return False
                    except Exception:
                        if filter_text not in data_str:
                            return False
                elif filter_text.startswith('>'):
                    filter_date = filter_text[1:].strip()
                    if data_str <= filter_date:
                        return False
                elif filter_text.startswith('<'):
                    filter_date = filter_text[1:].strip()
                    if data_str >= filter_date:
                        return False
                elif filter_text not in data_str:
                    return False
                
            elif column in [7, 8]:
                try:
                    numeric_part = ''.join(c for c in data_str if c.isdigit() or c == '.')
                    if not numeric_part:
                        return False
                    value = float(numeric_part)
                    
                    if '-' in filter_text and not filter_text.startswith('>') and not filter_text.startswith('<'):
                        try:
                            min_val, max_val = filter_text.split('-')
                            min_val = min_val.strip()
                            max_val = max_val.strip()
                            
                            min_val = float(min_val) if min_val else 0
                            max_val = float(max_val) if max_val else float('inf')
                            
                            if not (min_val <= value <= max_val):
                                return False
                        except ValueError:
                            if filter_text not in data_str:
                                return False
                    elif filter_text.startswith('>'):
                        min_val = float(filter_text[1:].strip())
                        if value <= min_val:
                            return False
                    elif filter_text.startswith('<'):
                        max_val = float(filter_text[1:].strip())
                        if value >= max_val:
                            return False
                    elif filter_text.isdigit():
                        if value != float(filter_text):
                            return False
                    else:
                        if filter_text not in data_str:
                            return False
                except (ValueError, TypeError):
                    if filter_text not in data_str:
                        return False
            
            elif '-' in filter_text and not filter_text.startswith('>') and not filter_text.startswith('<'):
                try:
                    start_text, end_text = filter_text.split('-')
                    start_text = start_text.strip()
                    end_text = end_text.strip()
                    
                    if start_text and end_text:
                        if not (start_text <= data_str <= end_text):
                            return False
                    elif start_text:
                        if data_str < start_text:
                            return False
                    elif end_text:
                        if data_str > end_text:
                            return False
                except Exception:
                    if filter_text not in data_str:
                        return False
            else:
                if filter_text not in data_str:
                    return False
        return True