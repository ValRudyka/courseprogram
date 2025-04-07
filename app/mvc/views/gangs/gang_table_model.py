from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class GangTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = [
            "ID", 
            "Назва", 
            "Дата заснування", 
            "Кількість членів", 
            "Основна діяльність", 
            "Місце бази",
            "Активних членів",
            "Лідер"
        ]
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
        not (0 <= index.row() < len(self._data)) or \
        not (0 <= index.column() < len(self._headers)):
            return None
        
        row = index.row()
        col = index.column()
        gang = self._data[row]
        
        if role == Qt.DisplayRole:
            if col == 0:
                return str(gang.get("id", ""))
            elif col == 1:
                return gang.get("name", "")
            elif col == 2: 
                return gang.get("founding_date", "")
            elif col == 3:
                return str(gang.get("number_of_members", ""))
            elif col == 4:
                return gang.get("main_activity", "")
            elif col == 5: 
                return gang.get("base_location", "")
            elif col == 6: 
                return str(gang.get("active_members", ""))
            elif col == 7:
                return gang.get("leader_name", "Невідомо")
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
    
    def sort(self, column, order):
        """Sort table by given column and order."""
        self.layoutAboutToBeChanged.emit()
        
        sort_keys = [
            "id", "name", "founding_date", "number_of_members", 
            "main_activity", "base_location", "active_members", "leader_name"
        ]
        
        if 0 <= column < len(sort_keys):
            key = sort_keys[column]
            reverse = order == Qt.DescendingOrder
            
            self._data.sort(
                key=lambda x: (x.get(key) is None, x.get(key)),
                reverse=reverse
            )
        
        self.layoutChanged.emit()
    
    def update_data(self, data):
        """Update the model with new data."""
        self.beginResetModel()
        self._data = data
        self.endResetModel()