import sys
import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication
# from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

from mvc.models.database import DatabaseConnector
from mvc.models.users import UserModel
from mvc.controllers.authcontroller import AuthController
from mvc.views.auth.register.register import RegisterView
from mvc.views.navigate.navigation_service import NavigationService

load_dotenv()

def main():
    app = QApplication(sys.argv)
    
    db_connector = DatabaseConnector()
    db_uri = f"""postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:
                {os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"""
    connection_success = db_connector.connect(db_uri)
    
    if not connection_success:
        return 1
    
    user_model = UserModel(db_connector)
    auth_controller = AuthController(user_model)
    nav_service = NavigationService()
    
    register_view = RegisterView()
    
    nav_service.register_view('register', register_view)
    nav_service.register_view('main', register_view)

    
    register_view.register_requested.connect(auth_controller.register_user)
    auth_controller.registration_success.connect(lambda _: register_view.show_success())
    auth_controller.registration_failed.connect(register_view.show_error)
    
    auth_controller.show_main_window.connect(nav_service.show_main_window)
    register_view.switch_to_login.connect(lambda: nav_service.show_view('login'))
    
    nav_service.show_view('register')
    
    result = app.exec()    
    db_connector.close()
    
    return result

if __name__ == "__main__":
    sys.exit(main())
