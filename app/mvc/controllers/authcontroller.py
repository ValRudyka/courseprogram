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
        self.current_user = None
    
    @Slot(str, str)
    def register_user(self, username, password):
        success, message = self.user_model.create_user(username, password)
        if success:            
                self.registration_success.emit(None) 
                self.show_main_window.emit(None)
        else:
            self.registration_failed.emit(message)
    
    @Slot(str, str)
    def authenticate_user(self, username, password):
        success, result = self.user_model.authenticate(username, password)
        
        if success:
            self.login_success.emit(result)
            self.show_main_window.emit(result)
        else:
            self.login_failed.emit(result)
    
    def is_authenticated(self):
        return self.current_user is not None