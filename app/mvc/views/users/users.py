from PySide6.QtWidgets import QMainWindow, QMessageBox, QAbstractItemView
from PySide6.QtCore import Signal
from .users_source import Ui_MainWindow
from .users_table import UsersTableModel

class UsersView(QMainWindow):
    add_user_requested = Signal()
    delete_user_requested = Signal(int)
    search_user_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.selected_user_id = None
        
        self.setup_connections()
        
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
    
    def setup_connections(self):
        self.ui.pushButton_3.clicked.connect(self.on_add_user)
        self.ui.pushButton_2.clicked.connect(self.on_delete_user)
        self.ui.lineEdit.textChanged.connect(self.on_search_text_changed)
        self.ui.tableView.clicked.connect(self.on_table_clicked)
    
    def on_table_clicked(self, index):
        if not index.isValid():
            return
            
        id_index = self.ui.tableView.model().index(index.row(), 0)
        self.selected_user_id = int(self.ui.tableView.model().data(id_index))
    
    def on_search_text_changed(self):
        search_text = self.ui.lineEdit.text().strip()
        self.search_user_requested.emit(search_text)
    
    def on_add_user(self):
        self.add_user_requested.emit()
    
    def on_delete_user(self):
        if self.selected_user_id is None:
            QMessageBox.warning(self, "Попередження", "Виберіть користувача для видалення")
            return
        
        index = self.ui.tableView.selectionModel().selectedRows()[0]
        username_index = self.ui.tableView.model().index(index.row(), 1)
        username = self.ui.tableView.model().data(username_index)
        
        reply = QMessageBox.warning(
            self, 
            "Підтвердження видалення", 
            f"Ви впевнені, що хочете видалити користувача '{username}'? Ця дія не може бути скасована.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.delete_user_requested.emit(self.selected_user_id)
    
    def set_users_data(self, users, current_username):
        """Set data for the users table."""
        filtered_users = [user for user in users if user.get("username") != current_username]
        
        model = UsersTableModel(filtered_users, current_username)
        self.ui.tableView.setModel(model)
        
        self.ui.tableView.setColumnWidth(0, 60)  
        self.ui.tableView.setColumnWidth(1, 200) 
        self.ui.tableView.setColumnWidth(2, 200) 
        self.ui.tableView.setColumnWidth(3, 150)
        
        self.ui.tableView.verticalHeader().setVisible(False)
        self.selected_user_id = None