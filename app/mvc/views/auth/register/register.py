from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal
from .register_source import Ui_RegisterWindow

class RegisterView(QMainWindow):
    register_requested = Signal(str, str)
    switch_to_login = Signal()           
    return_to_users_view_requested = Signal()
    
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
            
        self.ui.register_btn.clicked.connect(self._on_register)
    
    def _on_register(self) -> None:
        username = self.ui.username_edit.text().strip()
        password = self.ui.password_edit.text()
        
        if not username:
            self.show_error("Ім'я акаунту не може бути порожнім")
            return
            
        if not password:
            self.show_error("Пароль не може бути порожнім")
            return
        
        self.register_requested.emit(username, password)
    
    def _on_switch_to_login(self) -> None:
        self.clear()
        self.switch_to_login.emit()
    
    def show_error(self, message) -> None:
        QMessageBox.critical(self, "Помилка реєстрації", message)
    
    def show_success(self, message=None) -> None:
        if not message:
            message = "Реєстрація успішна! Відбувається вхід в систему."
            
        QMessageBox.information(self, "Успішна реєстрація", message)
    
    def return_to_users_view(self):
        self.clear()
        self.return_to_users_view_requested.emit()


    def clear(self) -> None:
        self.ui.username_edit.clear()
        self.ui.password_edit.clear()