from PySide6.QtCore import QObject, Signal, Slot
import logging

class AuthController(QObject):
    registration_success = Signal(object)  
    registration_failed = Signal(str)     
    login_success = Signal(object)        
    login_failed = Signal(str)            
    show_main_window = Signal(object)     
    
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.logger = logging.getLogger(__name__)
        self.current_user = None
    
    @Slot(str, str)
    def register_user(self, username, password):
        self.logger.info(f"Attempting to register user: {username}")
        
        success, message = self.user_model.create_user(username, password)
        
        if success:
            self.logger.info(f"User registration successful: {username}")
            
            auth_success, result = self.user_model.authenticate(username, password)
            
            if auth_success:
                self.current_user = result
                self.registration_success.emit(result) 
                
                self.show_main_window.emit(result)
            else:
                self.registration_failed.emit("Реєстрація успішна, але виникла проблема з входом. Спробуйте увійти вручну.")
        else:
            self.logger.warning(f"User registration failed: {username} - {message}")
            self.registration_failed.emit(message)
    
    @Slot(str, str)
    def authenticate_user(self, username, password):
        self.logger.info(f"Attempting to authenticate user: {username}")
        
        success, result = self.user_model.authenticate(username, password)
        
        if success:
            self.current_user = result
            self.logger.info(f"User authentication successful: {username}")
            self.login_success.emit(result)
            
            self.show_main_window.emit(result)
        else:
            self.logger.warning(f"User authentication failed: {username} - {result}")
            self.login_failed.emit(result)
    
    def is_authenticated(self):
        return self.current_user is not None