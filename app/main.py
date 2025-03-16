import sys
import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from mvc.models.database import DatabaseConnector
from mvc.models.users import UserModel
from mvc.controllers.authcontroller import AuthController
from mvc.views.auth.register.register import RegisterView
from mvc.views.auth.login.login import LoginView
from mvc.views.navigate.navigation_service import NavigationService

load_dotenv()

def main() -> int:
    app = QApplication(sys.argv)
    
    db_connector = DatabaseConnector()
    db_uri = f"""postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:
                {os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"""
    db_connector.connect_engine(db_uri)
    
    user_model = UserModel(db_connector.engine)
    auth_controller = AuthController(user_model)
    nav_service = NavigationService()
    register_view = RegisterView()
    login_view = LoginView()
    
    nav_service.register_view('register', register_view)
    nav_service.register_view('login', login_view)
    
    register_view.register_requested.connect(auth_controller.register_user)
    auth_controller.registration_success.connect(lambda _: register_view.show_success())
    auth_controller.registration_failed.connect(register_view.show_error)

    login_view.login_requested.connect(auth_controller.authenticate_user)
    auth_controller.login_success.connect(lambda _: login_view.clear())
    auth_controller.login_failed.connect(login_view.show_error)

    auth_controller.show_main_window.connect(nav_service.show_main_window)
    register_view.switch_to_login.connect(lambda: nav_service.show_view('login'))
    login_view.switch_to_register.connect(lambda: nav_service.show_view('register'))
    
    nav_service.show_view('login')
    
    result = app.exec()    
    db_connector.close()
    
    return result

if __name__ == "__main__":
    sys.exit(main())
