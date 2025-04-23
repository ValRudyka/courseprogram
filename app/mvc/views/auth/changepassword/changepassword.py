from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal
from .chanegpassword_source import Ui_MainWindow

class ChangePasswordView(QMainWindow):
    change_password_requested = Signal(str, str)
    cancel_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton_1.clicked.connect(self._on_change_password)
        
    def _on_change_password(self):
        """Handle password change button click."""
        new_password = self.ui.lineEdit.text()
        confirm_password = self.ui.lineEdit_2.text()
        
        # Validate input
        if not new_password:
            self.show_error("Новий пароль не може бути порожнім")
            return
            
        if not confirm_password:
            self.show_error("Підтвердження паролю не може бути порожнім")
            return
        
        if new_password != confirm_password:
            self.show_error("Паролі не співпадають")
            return
        
        # Emit signal with new password
        self.change_password_requested.emit(new_password, confirm_password)
    
    def show_error(self, message):
        """Display error message."""
        QMessageBox.critical(self, "Помилка зміни паролю", message)
    
    def show_success(self, message=None):
        """Display success message."""
        if not message:
            message = "Пароль успішно змінено!"
        QMessageBox.information(self, "Успішна зміна паролю", message)
        self.clear()
    
    def clear(self):
        """Clear form inputs."""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()