from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel
from PySide6.QtCore import Signal, Qt
from .login_source import Ui_MainWindow

class LoginView(QMainWindow):
    login_requested = Signal(str, str)    
    switch_to_register = Signal()           
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.status_label = QLabel(self.ui.centralwidget)
        self.status_label.setGeometry(60, 430, 500, 30)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        
        self.ui.login_btn.clicked.connect(self._on_login)
        
        self.ui.password_edit.returnPressed.connect(self._on_login)
    
    def _on_login(self):
        username = self.ui.username_edit.text().strip()
        password = self.ui.password_edit.text()
        
        if not username:
            self.show_error("Ім'я акаунту не може бути порожнім")
            return
            
        if not password:
            self.show_error("Пароль не може бути порожнім")
            return
        
        self.show_status("Виконується вхід...", "#0066cc")
        self.ui.login_btn.setEnabled(False)
        
        self.login_requested.emit(username, password)
    
    def _on_switch_to_register(self):
        self.clear()
        self.switch_to_register.emit()
    
    def show_error(self, message):
        """Display error message with visual indication"""
        self.ui.login_btn.setEnabled(True) 
        
        if "акаунту" in message:
            self.highlight_field(self.ui.username_edit)
        elif "пароль" in message.lower():
            self.highlight_field(self.ui.password_edit)
        
        QMessageBox.critical(self, "Помилка входу", message)
        self.show_status(message, "#cc0000")
    
    def show_success(self, message="Успішний вхід!"):
        """Display success message"""
        self.ui.login_btn.setEnabled(True)
        self.show_status(message, "#009900")
    
    def show_status(self, message, color="#000000"):
        """Show a status message with specified color"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.status_label.setVisible(True)
    
    def highlight_field(self, field):
        """Highlight a field with red background to indicate error"""
        field.setStyleSheet("background-color: #fff0f0; border: 1px solid #ffcccc;")
        
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: field.setStyleSheet(""))
    
    def clear(self):
        """Clear form inputs and reset status"""
        self.ui.username_edit.clear()
        self.ui.password_edit.clear()
        self.status_label.setVisible(False)
        self.status_label.setText("")
        self.status_label.setVisible(True)
        self.ui.login_btn.setEnabled(True)