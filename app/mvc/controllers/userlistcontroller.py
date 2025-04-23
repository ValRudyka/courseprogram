from PySide6.QtCore import QObject, Signal, Slot

class UserListController(QObject):
    users_loaded = Signal(list, str)
    user_deleted = Signal(int)
    operation_error = Signal(str)
    
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.current_username = None
    
    def set_current_user(self, username):
        self.current_username = username
    
    def get_all_users(self, search_filter=None):
        try:
            users = self.user_model.get_all_users(search_filter)
            self.users_loaded.emit(users, self.current_username)
            return users
        except Exception as e:
            self.operation_error.emit(f"Помилка завантаження користувачів: {str(e)}")
            return []
    
    @Slot(str)
    def search_users(self, search_text):
        self.get_all_users(search_text)
    
    @Slot(int)
    def delete_user(self, user_id):
        try:
            success, message = self.user_model.delete_user(user_id)
            if success:
                self.user_deleted.emit(user_id)
                return True
            else:
                self.operation_error.emit(message)
                return False
        except Exception as e:
            self.operation_error.emit(f"Error deleting user: {str(e)}")
            return False