import sys
import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMessageBox

from mvc.models.database import DatabaseConnector
from mvc.models.users import UserModel
from mvc.models.criminals import CriminalModel

from mvc.controllers.authcontroller import AuthController
from mvc.controllers.criminalcontroller import CriminalController

from mvc.views.auth.register.register import RegisterView
from mvc.views.auth.login.login import LoginView
from mvc.views.criminals.criminal_info import CriminalsView
from mvc.views.gangs.gang_info import GangsView
from mvc.views.archive.archive_info import ArchiveView
from mvc.views.mainwindow import MainWindow

from mvc.views.criminals.criminal_manipulation.criminal_add_form import CriminalAddForm
from mvc.views.criminals.criminal_manipulation.criminal_edit_form import CriminalEditForm

load_dotenv()

def main() -> int:
    app = QApplication(sys.argv)
    
    db_connector = DatabaseConnector()
    db_uri = f"""postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"""
    connected = db_connector.connect_engine(db_uri)
    
    if not connected:
        QMessageBox.critical(None, "Database Error", "Could not connect to database. Please check your connection settings.")
        return 1
    
    user_model = UserModel(db_connector.engine)
    criminal_model = CriminalModel(db_connector.engine)
    
    auth_controller = AuthController(user_model)
    criminal_controller = CriminalController(criminal_model)
    
    register_view = RegisterView()
    login_view = LoginView()
    criminals_view = CriminalsView()
    gangs_view = GangsView()
    archive_view = ArchiveView()
    main_view = MainWindow()
    
    criminal_add_form = CriminalAddForm()
    criminal_edit_form = CriminalEditForm()
    
    login_view.login_requested.connect(auth_controller.authenticate_user)
    auth_controller.login_success.connect(lambda _: login_view.clear())
    auth_controller.login_failed.connect(login_view.show_error)
    
    register_view.register_requested.connect(auth_controller.register_user)
    auth_controller.registration_success.connect(lambda _: register_view.show_success())
    auth_controller.registration_failed.connect(register_view.show_error)
    
    auth_controller.show_main_window.connect(lambda: (login_view.hide(), main_view.show()))
    register_view.switch_to_login.connect(lambda: (register_view.hide(), login_view.show()))
    login_view.switch_to_register.connect(lambda: (login_view.hide(), register_view.show()))
    
    main_view.open_criminals_requested.connect(lambda: (main_view.hide(), criminals_view.show()))
    main_view.open_groups_requested.connect(lambda: (main_view.hide(), gangs_view.show()))
    main_view.open_archive_requested.connect(lambda: (main_view.hide(), archive_view.show()))
    
    criminals_view.add_criminal_requested.connect(lambda: (
    criminal_add_form.load_reference_data(
        criminal_controller.get_cities(),
        criminal_controller.get_professions(),
        criminal_controller.get_criminal_groups(),
        criminal_controller.get_languages()
    ),
        criminals_view.hide(),
        criminal_add_form.show()
    ))

    criminals_view.edit_criminal_requested.connect(lambda criminal_id: (
        criminal_edit_form.load_reference_data(
            criminal_controller.get_cities(),
            criminal_controller.get_professions(),
            criminal_controller.get_criminal_groups(),
            criminal_controller.get_languages()
        ),
        criminal_edit_form.set_criminal_data(criminal_id, criminal_controller.get_criminal(criminal_id)),
        criminals_view.hide(),
        criminal_edit_form.show()
    ))

    criminals_view.export_criminals_requested.connect(lambda include_archived: (
        criminals_view.export_criminals_data(
            criminal_controller.get_criminals_for_export(include_archived)
        )
    ))
    
    # Connect archive and delete actions
    criminals_view.archive_criminal_requested.connect(criminal_controller.archive_criminal)
    criminals_view.delete_criminal_requested.connect(criminal_controller.delete_criminal)
    
    # Connect save/update actions from forms
    criminal_add_form.save_requested.connect(criminal_controller.add_criminal)
    criminal_edit_form.update_requested.connect(criminal_controller.update_criminal)
    
    # Connect controller result signals
    criminal_controller.criminal_added.connect(lambda _: (
        QMessageBox.information(criminal_add_form, "Success", "Злочинець успішно доданий"),
        criminal_add_form.reset_form(),
        criminal_add_form.hide(),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals()),
        criminals_view.show()
    ))
    
    criminal_controller.criminal_updated.connect(lambda _: (
        QMessageBox.information(criminal_edit_form, "Success", "Інформація про злочинця успішно оновлена"),
        criminal_edit_form.hide(),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals()),
        criminals_view.show()
    ))
    
    criminal_controller.criminal_archived.connect(lambda _: (
        QMessageBox.information(criminals_view, "Success", "Злочинець архівований"),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    ))
    
    criminal_controller.criminal_deleted.connect(lambda _: (
        QMessageBox.information(criminals_view, "Success", "Злочинець видалений"),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    ))
    
    # Connect error handling
    criminal_controller.operation_error.connect(lambda error_msg: 
        QMessageBox.critical(None, "Error", error_msg)
    )
    
    def handle_main_close():
        app.quit() 
    
    def handle_criminals_close():
        criminals_view.hide()
        main_view.show()
    
    def handle_gangs_close():
        gangs_view.hide()
        main_view.show()
    
    def handle_archive_close():
        archive_view.hide()
        main_view.show()
    
    def handle_add_form_close():
        criminal_add_form.hide()
        criminals_view.show()
    
    def handle_edit_form_close():
        criminal_edit_form.hide()
        criminals_view.show()
    
    main_view.closeEvent = lambda event: handle_main_close()
    criminals_view.closeEvent = lambda event: handle_criminals_close()
    gangs_view.closeEvent = lambda event: handle_gangs_close()
    archive_view.closeEvent = lambda event: handle_archive_close()
    criminal_add_form.closeEvent = lambda event: handle_add_form_close()
    criminal_edit_form.closeEvent = lambda event: handle_edit_form_close()
    
    login_view.show()
    
    criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    
    result = app.exec()
    
    db_connector.close()
    
    return result

if __name__ == "__main__":
    sys.exit(main())