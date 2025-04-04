from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class CriminalTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = [
            "ID", 
            "Ім'я", 
            "Прізвище", 
            "Кличка", 
            "Дата народження", 
            "Місце народження", 
            "Місце проживання",
            "Зріст",
            "Вага"
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
            # Return formatted data based on column
            if col == 0:  # ID
                return str(criminal.get("id_criminal", ""))
            elif col == 1:  # First name
                return criminal.get("first_name", "")
            elif col == 2:  # Last name
                return criminal.get("last_name", "")
            elif col == 3:  # Nickname
                return criminal.get("nickname", "")
            elif col == 4:  # Birth date
                return criminal.get("date_of_birth", "")
            elif col == 5:  # Birth place
                return criminal.get("birth_place", "")
            elif col == 6:  # Residence
                return criminal.get("residence", "")
            elif col == 7:  # Height
                return f"{criminal.get('height', '')} см" if criminal.get('height') else ""
            elif col == 8:  # Weight
                return f"{criminal.get('weight', '')} кг" if criminal.get('weight') else ""
        
        elif role == Qt.TextAlignmentRole:
            # Center align numeric columns
            if col in [0, 7, 8]:  # ID, Height, Weight
                return Qt.AlignCenter
        
        elif role == Qt.BackgroundRole:
            # Highlight archived criminals
            if criminal.get("is_archived"):
                return Qt.lightGray
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
    
    def sort(self, column, order):
        """Sort table by given column and order."""
        self.layoutAboutToBeChanged.emit()
        
        # Map column to sorting key
        sort_keys = [
            "id_criminal", "first_name", "last_name", "nickname", 
            "date_of_birth", "birth_place", "residence", "height", "weight"
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