from PySide6.QtCore import QObject, Signal, Slot
from mvc.models.users import UserModel

class UserController(QObject):
    password_changed = Signal(bool, str)
    
    def __init__(self, user_model: UserModel) -> None:
        super().__init__()
        self.user_model = user_model
        self.current_username = None
    
    def set_current_user(self, username: str) -> None:
        """Set the current username for operations."""
        self.current_username = username
    
    @Slot(str, str)
    def change_password(self, new_password: str, confirm_password: str) -> None:
        """Change the password for the current user."""
        if not self.current_username:
            self.password_changed.emit(False, "Спочатку увійдіть в систему")
            return
            
        if new_password != confirm_password:
            self.password_changed.emit(False, "Паролі не співпадають")
            return
            
        success, message = self.user_model.change_password(self.current_username, new_password)
        self.password_changed.emit(success, message)