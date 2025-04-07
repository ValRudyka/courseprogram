import sys
import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMessageBox

from mvc.models.database import DatabaseConnector
from mvc.models.users import UserModel
from mvc.models.criminals import CriminalModel
from mvc.models.cities import CityModel
from mvc.models.languages import LanguageModel
from mvc.models.professions import ProfessionModel
from mvc.models.criminal_gangs import CriminalGroupModel

from mvc.controllers.authcontroller import AuthController
from mvc.controllers.criminalcontroller import CriminalController
from mvc.controllers.gangcontroller import GangController
from mvc.controllers.archivecontroller import ArchiveController


from mvc.views.auth.register.register import RegisterView
from mvc.views.auth.login.login import LoginView
from mvc.views.criminals.criminal_info import CriminalsView
from mvc.views.gangs.gang_info import GangsView
from mvc.views.archive.archive_info import ArchiveView
from mvc.views.mainwindow import MainWindow

from mvc.views.criminals.criminal_manipulation.criminal_add_form import CriminalAddForm
from mvc.views.criminals.criminal_manipulation.criminal_edit_form import CriminalEditForm
from mvc.views.gangs.gang_manipulation.gang_add_form import GangAddForm
from mvc.views.gangs.gang_manipulation.gang_edit_form import GangEditForm

from mvc.views.navigate.navigation_service import NavigationService

load_dotenv()

def main() -> int:
    app = QApplication(sys.argv)
    
    # Initialize the NavigationService
    navigation_service = NavigationService()
    
    # Database connection
    db_connector = DatabaseConnector()
    db_uri = f"""postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"""
    connected = db_connector.connect_engine(db_uri)
    
    if not connected:
        QMessageBox.critical(None, "Database Error", "Could not connect to database. Please check your connection settings.")
        return 1
    
    # Initialize models
    user_model = UserModel(db_connector.engine)
    criminal_model = CriminalModel(db_connector.engine)
    city_model = CityModel(db_connector.engine)
    language_model = LanguageModel(db_connector.engine)
    profession_model = ProfessionModel(db_connector.engine)
    criminal_group_model = CriminalGroupModel(db_connector.engine)
    
    # Initialize controllers
    auth_controller = AuthController(user_model)
    criminal_controller = CriminalController(
        criminal_model,
        city_model,
        profession_model,
        language_model,
        criminal_group_model
    )
    gang_controller = GangController(criminal_group_model, city_model)
    archive_controller = ArchiveController(criminal_model)

    
    # Initialize views
    register_view = RegisterView()
    login_view = LoginView()
    criminals_view = CriminalsView()
    gangs_view = GangsView()
    archive_view = ArchiveView()
    main_view = MainWindow()
    
    criminal_add_form = CriminalAddForm()
    criminal_edit_form = CriminalEditForm()
    gang_add_form = GangAddForm()
    gang_edit_form = GangEditForm()

    navigation_service.register_view("login", login_view)
    navigation_service.register_view("register", register_view)
    navigation_service.register_view("main", main_view)
    navigation_service.register_view("criminals", criminals_view)
    navigation_service.register_view("gangs", gangs_view)
    navigation_service.register_view("archive", archive_view)
    navigation_service.register_view("criminal_add", criminal_add_form)
    navigation_service.register_view("criminal_edit", criminal_edit_form)
    navigation_service.register_view("gang_add", gang_add_form)
    navigation_service.register_view("gang_edit", gang_edit_form)
    
    navigation_service.register_transition("main", "criminals")
    navigation_service.register_transition("main", "gangs")
    navigation_service.register_transition("main", "archive")
    
    navigation_service.register_transition("criminals", "main")
    navigation_service.register_transition("gangs", "main")
    navigation_service.register_transition("archive", "main")
    
    navigation_service.register_transition("criminals", "criminal_add")
    navigation_service.register_transition("criminals", "criminal_edit")
    navigation_service.register_transition("criminal_add", "criminals")
    navigation_service.register_transition("criminal_edit", "criminals")
    
    navigation_service.register_transition("gangs", "gang_add")
    navigation_service.register_transition("gangs", "gang_edit")
    navigation_service.register_transition("gang_add", "gangs")
    navigation_service.register_transition("gang_edit", "gangs")
    
    navigation_service.register_transition("login", "register")
    navigation_service.register_transition("register", "login")
    navigation_service.register_transition("login", "main")
    
    login_view.login_requested.connect(auth_controller.authenticate_user)
    auth_controller.login_success.connect(lambda _: login_view.clear())
    auth_controller.login_failed.connect(login_view.show_error)
    
    register_view.register_requested.connect(auth_controller.register_user)
    auth_controller.registration_success.connect(lambda _: register_view.show_success())
    auth_controller.registration_failed.connect(register_view.show_error)
    
    auth_controller.show_main_window.connect(lambda: navigation_service.navigate_to("main", "login"))
    register_view.switch_to_login.connect(lambda: navigation_service.navigate_to("login", "register"))
    login_view.switch_to_register.connect(lambda: navigation_service.navigate_to("register", "login"))
    
    main_view.open_criminals_requested.connect(lambda: navigation_service.navigate_to("criminals", "main"))
    main_view.open_groups_requested.connect(lambda: (
        gangs_view.set_gangs_data(gang_controller.get_all_gangs()),
        navigation_service.navigate_to("gangs", "main")
    ))
    main_view.open_archive_requested.connect(lambda: navigation_service.navigate_to("archive", "main"))
    
    criminals_view.add_criminal_requested.connect(lambda: (
        criminal_add_form.load_reference_data(
            criminal_controller.get_cities(),
            criminal_controller.get_professions(),
            criminal_controller.get_criminal_groups(),
            criminal_controller.get_languages()
        ),
        navigation_service.navigate_to("criminal_add", "criminals")
    ))

    criminals_view.edit_criminal_requested.connect(lambda criminal_id: (
        criminal_edit_form.load_reference_data(
            criminal_controller.get_cities(),
            criminal_controller.get_professions(),
            criminal_controller.get_criminal_groups(),
            criminal_controller.get_languages()
        ),
        criminal_edit_form.set_criminal_data(criminal_id, criminal_controller.get_criminal(criminal_id)),
        navigation_service.navigate_to("criminal_edit", "criminals")
    ))

    criminals_view.export_criminals_requested.connect(lambda include_archived: (
        criminals_view.export_criminals_data(
            criminal_controller.get_criminals_for_export(include_archived)
        )
    ))
    
    criminals_view.archive_criminal_requested.connect(criminal_controller.archive_criminal)
    criminals_view.delete_criminal_requested.connect(criminal_controller.delete_criminal)
    
    criminal_add_form.save_requested.connect(criminal_controller.add_criminal)
    criminal_edit_form.update_requested.connect(criminal_controller.update_criminal)
    
    gangs_view.add_gang_requested.connect(lambda: (
        gang_add_form.load_reference_data(gang_controller.get_cities()),
        navigation_service.navigate_to("gang_add", "gangs")
    ))
    
    gangs_view.edit_gang_requested.connect(lambda gang_id: (
        gang_edit_form.load_reference_data(gang_controller.get_cities()),
        gang_edit_form.set_gang_data(gang_id, gang_controller.get_gang(gang_id)),
        navigation_service.navigate_to("gang_edit", "gangs")
    ))
    
    gangs_view.delete_gang_requested.connect(gang_controller.delete_gang)
    
    gangs_view.export_gangs_requested.connect(lambda: (
        gangs_view.export_gangs_data(gang_controller.get_gangs_for_export())
    ))
    
    gang_add_form.save_requested.connect(gang_controller.add_gang)
    gang_edit_form.update_requested.connect(gang_controller.update_gang)
    
    criminal_controller.criminal_added.connect(lambda _: (
        QMessageBox.information(criminal_add_form, "Success", "Злочинець успішно доданий"),
        criminal_add_form.reset_form(),
        navigation_service.navigate_to("criminals", "criminal_add"),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    ))
    
    criminal_controller.criminal_updated.connect(lambda _: (
        QMessageBox.information(criminal_edit_form, "Success", "Інформація про злочинця успішно оновлена"),
        navigation_service.navigate_to("criminals", "criminal_edit"),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    ))
    
    criminal_controller.criminal_archived.connect(lambda _: (
        QMessageBox.information(criminals_view, "Success", "Злочинець архівований"),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    ))
    
    criminal_controller.criminal_deleted.connect(lambda _: (
        QMessageBox.information(criminals_view, "Success", "Злочинець видалений"),
        criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    ))
    
    criminal_controller.operation_error.connect(lambda error_msg: 
        QMessageBox.critical(None, "Error", error_msg)
    )
    
    gang_controller.gang_added.connect(lambda _: (
        QMessageBox.information(gang_add_form, "Success", "Угруповання успішно додане"),
        gang_add_form.reset_form(),
        navigation_service.navigate_to("gangs", "gang_add"),
        gangs_view.set_gangs_data(gang_controller.get_all_gangs())
    ))
    
    gang_controller.gang_updated.connect(lambda _: (
        QMessageBox.information(gang_edit_form, "Success", "Інформація про угруповання успішно оновлена"),
        navigation_service.navigate_to("gangs", "gang_edit"),
        gangs_view.set_gangs_data(gang_controller.get_all_gangs())
    ))
    
    gang_controller.gang_deleted.connect(lambda _: (
        QMessageBox.information(gangs_view, "Success", "Угруповання видалене"),
        gangs_view.set_gangs_data(gang_controller.get_all_gangs())
    ))
    
    gang_controller.operation_error.connect(lambda error_msg: 
        QMessageBox.critical(None, "Error", error_msg)
    )

    archive_view.delete_archived_criminal_requested.connect(archive_controller.delete_archived_criminal)

    archive_controller.criminal_deleted.connect(lambda _: (
        QMessageBox.information(archive_view, "Success", "Злочинець повністю видалений з архіву"),
        archive_view.set_archive_data(archive_controller.get_archived_criminals())
    ))
    
    archive_controller.operation_error.connect(lambda error_msg: 
        QMessageBox.critical(None, "Error", error_msg)
    )
    
    main_view.open_archive_requested.connect(lambda: (
        archive_view.set_archive_data(archive_controller.get_archived_criminals()),
        navigation_service.navigate_to("archive", "main")
    ))

    navigation_service.setup_close_handlers(app)
    
    criminals_view.set_criminals_data(criminal_controller.get_all_criminals())
    
    login_view.show()
    navigation_service.current_view = "login"
    
    result = app.exec()
    db_connector.close()
    
    return result

if __name__ == "__main__":
    sys.exit(main())