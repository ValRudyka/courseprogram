from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class UsersTableModel(QAbstractTableModel):
    def __init__(self, data=None, current_username=None):
        super().__init__()
        self._data = data or []
        self._headers = ["ID", "Логін", "Останній вхід", "Невдалі спроби"]
        self.current_username = current_username
        
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
        user = self._data[row]
        
        if role == Qt.DisplayRole:
            if col == 0:
                return str(user.get("user_id", ""))
            elif col == 1:
                return user.get("username", "")
            elif col == 2:
                return user.get("last_login", "")
            elif col == 3:
                return str(user.get("failed_attempts", "0"))
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
    
    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        
        sort_keys = [
            "user_id", "username", "last_login", "failed_attempts"
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
        self.beginResetModel()
        self._data = data
        self.endResetModel()