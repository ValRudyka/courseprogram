from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class ArchiveTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = [
            "ID", 
            "Ім'я", 
            "Прізвище", 
            "Кличка", 
            "Місце народження",
            "Місце проживання",
            "Дата народження",
            "Зріст",
            "Вага",
            "Угруповання",
            "Дата архівації"
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
        criminal = self._data[row]
        
        if role == Qt.DisplayRole:
            if col == 0:
                return str(criminal.get("id_criminal", ""))
            elif col == 1:
                return criminal.get("first_name", "")
            elif col == 2: 
                return criminal.get("last_name", "")
            elif col == 3:
                return criminal.get("nickname", "")
            elif col == 4: 
                return criminal.get("birth_place", "")
            elif col == 5:
                return criminal.get("residence", "")
            elif col == 6:
                return criminal.get("date_of_birth", "")
            elif col == 7:
                height = criminal.get("height")
                return f"{height} см" if height else ""
            elif col == 8:
                weight = criminal.get("weight")
                return f"{weight} кг" if weight else ""
            elif col == 9:
                return criminal.get("group_name", "")
            elif col == 10:
                return criminal.get("archive_date", "")
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
    
    def sort(self, column, order):
        """Sort table by given column and order."""
        self.layoutAboutToBeChanged.emit()
        
        sort_keys = [
            "id_criminal", "first_name", "last_name", "nickname", 
            "birth_place", "residence", "date_of_birth", "height", "weight", 
            "group_name", "archive_date"
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