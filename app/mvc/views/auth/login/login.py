from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal
from .login_source import Ui_MainWindow

class LoginView(QMainWindow):
    login_requested = Signal(str, str)    
    switch_to_register = Signal()           
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.login_btn.clicked.connect(self._on_login)
        self.ui.pushButton_2.clicked.connect(self._on_switch_to_register)
    
    def _on_login(self):
        username = self.ui.username_edit.text().strip()
        password = self.ui.password_edit.text()
        
        if not username:
            self.show_error("Ім'я акаунту не може бути порожнім")
            return
            
        if not password:
            self.show_error("Пароль не може бути порожнім")
            return
        
        self.login_requested.emit(username, password)
    
    def _on_switch_to_register(self):
        self.switch_to_register.emit()
    
    def show_error(self, message):
        QMessageBox.critical(self, "Помилка входу", message)
    
    def clear(self):
        """Clear form inputs"""
        self.ui.username_edit.clear()
        self.ui.password_edit.clear()