from PySide6.QtWidgets import QMessageBox

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


class ApplicationInitializer:
    """Class responsible for initializing the MVC components of the application"""
    
    def __init__(self, app, db_uri):
        self.app = app
        self.db_uri = db_uri
        self.navigation = NavigationService()
        
        # Initialize all components
        self.init_database()
        self.init_models()
        self.init_controllers()
        self.init_views()
        self.init_forms()
        self.register_views()
        self.connect_signals()
        
    def init_database(self):
        """Initialize database connection"""
        self.db_connector = DatabaseConnector()
        connected = self.db_connector.connect_engine(self.db_uri)
        
        if not connected:
            QMessageBox.critical(None, "Database Error", 
                                "Could not connect to database. Please check your connection settings.")
            raise ConnectionError("Database connection failed")
            
    def init_models(self):
        """Initialize all models"""
        self.user_model = UserModel(self.db_connector.engine)
        self.criminal_model = CriminalModel(self.db_connector.engine)
        self.city_model = CityModel(self.db_connector.engine)
        self.language_model = LanguageModel(self.db_connector.engine)
        self.profession_model = ProfessionModel(self.db_connector.engine)
        self.criminal_group_model = CriminalGroupModel(self.db_connector.engine)
        
    def init_controllers(self):
        """Initialize all controllers"""
        self.auth_controller = AuthController(self.user_model)
        self.criminal_controller = CriminalController(
            self.criminal_model,
            self.city_model,
            self.profession_model,
            self.language_model,
            self.criminal_group_model
        )
        self.gang_controller = GangController(self.criminal_group_model, self.city_model)
        
    def init_views(self):
        """Initialize all main views"""
        self.register_view = RegisterView()
        self.login_view = LoginView()
        self.main_view = MainWindow()
        self.criminals_view = CriminalsView()
        self.gangs_view = GangsView()
        self.archive_view = ArchiveView()
        
    def init_forms(self):
        """Initialize all forms"""
        self.criminal_add_form = CriminalAddForm()
        self.criminal_edit_form = CriminalEditForm()
        self.gang_add_form = GangAddForm()
        self.gang_edit_form = GangEditForm()
        
    def register_views(self):
        """Register all views with the navigation service"""
        self.navigation.register_view('login', self.login_view)
        self.navigation.register_view('register', self.register_view)
        self.navigation.register_view('main', self.main_view)
        self.navigation.register_view('criminals', self.criminals_view)
        self.navigation.register_view('gangs', self.gangs_view)
        self.navigation.register_view('archive', self.archive_view)
        self.navigation.register_view('criminal_add', self.criminal_add_form)
        self.navigation.register_view('criminal_edit', self.criminal_edit_form)
        self.navigation.register_view('gang_add', self.gang_add_form)
        self.navigation.register_view('gang_edit', self.gang_edit_form)
        
        self.navigation.setup_close_handlers(self.app)
        
    def connect_signals(self):
        """Connect all signals between components"""
        self._connect_auth_signals()
        self._connect_main_signals()
        self._connect_criminals_signals()
        self._connect_gangs_signals()
        
    def _connect_auth_signals(self):
        """Connect authentication-related signals"""
        self.login_view.login_requested.connect(self.auth_controller.authenticate_user)
        self.auth_controller.login_success.connect(lambda _: self.login_view.clear())
        self.auth_controller.login_failed.connect(self.login_view.show_error)
        self.login_view.switch_to_register.connect(
            lambda: self.navigation.navigate_to('register', 'login'))
        
        self.register_view.register_requested.connect(self.auth_controller.register_user)
        self.auth_controller.registration_success.connect(
            lambda _: self.register_view.show_success())
        self.auth_controller.registration_failed.connect(self.register_view.show_error)
        self.register_view.switch_to_login.connect(
            lambda: self.navigation.navigate_to('login', 'register'))
        
        self.auth_controller.show_main_window.connect(
            lambda: self.navigation.navigate_to('main', self.navigation.current_view))
        
    def _connect_main_signals(self):
        """Connect main window navigation signals"""
        self.main_view.open_criminals_requested.connect(
            lambda: self.navigation.navigate_to('criminals', 'main'))
        
        self.main_view.open_groups_requested.connect(
            lambda: self._load_gangs_and_navigate())
        
        self.main_view.open_archive_requested.connect(
            lambda: self.navigation.navigate_to('archive', 'main'))
            
    def _load_gangs_and_navigate(self):
        """Load gangs data and navigate to gangs view"""
        self.gangs_view.set_gangs_data(self.gang_controller.get_all_gangs())
        self.navigation.navigate_to('gangs', 'main')
        
    def _connect_criminals_signals(self):
        """Connect criminals-related signals"""
        self.criminals_view.add_criminal_requested.connect(
            lambda: self._load_criminal_add_form())
        
        self.criminals_view.edit_criminal_requested.connect(
            lambda criminal_id: self._load_criminal_edit_form(criminal_id))
        
        self.criminals_view.export_criminals_requested.connect(
            lambda include_archived: self._export_criminals(include_archived))
        
        self.criminals_view.archive_criminal_requested.connect(
            self.criminal_controller.archive_criminal)
        
        self.criminals_view.delete_criminal_requested.connect(
            self.criminal_controller.delete_criminal)
        
        self.criminal_add_form.save_requested.connect(
            self.criminal_controller.add_criminal)
        
        self.criminal_edit_form.update_requested.connect(
            self.criminal_controller.update_criminal)
        
        self.criminal_controller.criminal_added.connect(
            lambda _: self._handle_criminal_added())
        
        self.criminal_controller.criminal_updated.connect(
            lambda _: self._handle_criminal_updated())
        
        self.criminal_controller.criminal_archived.connect(
            lambda _: self._handle_criminal_archived())
        
        self.criminal_controller.criminal_deleted.connect(
            lambda _: self._handle_criminal_deleted())
        
        self.criminal_controller.operation_error.connect(
            lambda error_msg: QMessageBox.critical(None, "Error", error_msg))
    
    def _load_criminal_add_form(self):
        """Load reference data for criminal add form and navigate to it"""
        self.criminal_add_form.load_reference_data(
            self.criminal_controller.get_cities(),
            self.criminal_controller.get_professions(),
            self.criminal_controller.get_criminal_groups(),
            self.criminal_controller.get_languages()
        )
        self.navigation.navigate_to('criminal_add', 'criminals')
    
    def _load_criminal_edit_form(self, criminal_id):
        """Load reference data for criminal edit form and navigate to it"""
        self.criminal_edit_form.load_reference_data(
            self.criminal_controller.get_cities(),
            self.criminal_controller.get_professions(),
            self.criminal_controller.get_criminal_groups(),
            self.criminal_controller.get_languages()
        )
        self.criminal_edit_form.set_criminal_data(
            criminal_id, 
            self.criminal_controller.get_criminal(criminal_id)
        )
        self.navigation.navigate_to('criminal_edit', 'criminals')
    
    def _export_criminals(self, include_archived):
        """Export criminals data"""
        self.criminals_view.export_criminals_data(
            self.criminal_controller.get_criminals_for_export(include_archived)
        )
    
    def _handle_criminal_added(self):
        """Handle successful criminal addition"""
        QMessageBox.information(self.criminal_add_form, "Success", 
                               "Злочинець успішно доданий")
        self.criminal_add_form.reset_form()
        self.criminals_view.set_criminals_data(self.criminal_controller.get_all_criminals())
        self.navigation.navigate_to('criminals', 'criminal_add')
    
    def _handle_criminal_updated(self):
        """Handle successful criminal update"""
        QMessageBox.information(self.criminal_edit_form, "Success", 
                               "Інформація про злочинця успішно оновлена")
        self.criminals_view.set_criminals_data(self.criminal_controller.get_all_criminals())
        self.navigation.navigate_to('criminals', 'criminal_edit')
    
    def _handle_criminal_archived(self):
        """Handle successful criminal archiving"""
        QMessageBox.information(self.criminals_view, "Success", 
                               "Злочинець архівований")
        self.criminals_view.set_criminals_data(self.criminal_controller.get_all_criminals())
    
    def _handle_criminal_deleted(self):
        """Handle successful criminal deletion"""
        QMessageBox.information(self.criminals_view, "Success", 
                               "Злочинець видалений")
        self.criminals_view.set_criminals_data(self.criminal_controller.get_all_criminals())
    
    def _connect_gangs_signals(self):
        """Connect gangs-related signals"""
        self.gangs_view.add_gang_requested.connect(
            lambda: self._load_gang_add_form())
        
        self.gangs_view.edit_gang_requested.connect(
            lambda gang_id: self._load_gang_edit_form(gang_id))
        
        self.gangs_view.delete_gang_requested.connect(
            self.gang_controller.delete_gang)
        
        self.gangs_view.export_gangs_requested.connect(
            lambda: self._export_gangs())
        
        self.gang_add_form.save_requested.connect(
            self.gang_controller.add_gang)
        
        self.gang_edit_form.update_requested.connect(
            self.gang_controller.update_gang)
        
        self.gang_controller.gang_added.connect(
            lambda _: self._handle_gang_added())
        
        self.gang_controller.gang_updated.connect(
            lambda _: self._handle_gang_updated())
        
        self.gang_controller.gang_deleted.connect(
            lambda _: self._handle_gang_deleted())
        
        self.gang_controller.operation_error.connect(
            lambda error_msg: QMessageBox.critical(None, "Error", error_msg))
    
    def _load_gang_add_form(self):
        """Load reference data for gang add form and navigate to it"""
        self.gang_add_form.load_reference_data(self.gang_controller.get_cities())
        self.navigation.navigate_to('gang_add', 'gangs')
    
    def _load_gang_edit_form(self, gang_id):
        """Load reference data for gang edit form and navigate to it"""
        self.gang_edit_form.load_reference_data(self.gang_controller.get_cities())
        self.gang_edit_form.set_gang_data(gang_id, self.gang_controller.get_gang(gang_id))
        self.navigation.navigate_to('gang_edit', 'gangs')
    
    def _export_gangs(self):
        """Export gangs data"""
        self.gangs_view.export_gangs_data(self.gang_controller.get_gangs_for_export())
    
    def _handle_gang_added(self):
        """Handle successful gang addition"""
        QMessageBox.information(self.gang_add_form, "Success", 
                               "Угруповання успішно додане")
        self.gang_add_form.reset_form()
        self.gangs_view.set_gangs_data(self.gang_controller.get_all_gangs())
        self.navigation.navigate_to('gangs', 'gang_add')
    
    def _handle_gang_updated(self):
        """Handle successful gang update"""
        QMessageBox.information(self.gang_edit_form, "Success", 
                               "Інформація про угруповання успішно оновлена")
        self.gangs_view.set_gangs_data(self.gang_controller.get_all_gangs())
        self.navigation.navigate_to('gangs', 'gang_edit')
    
    def _handle_gang_deleted(self):
        """Handle successful gang deletion"""
        QMessageBox.information(self.gangs_view, "Success", 
                               "Угруповання видалене")
        self.gangs_view.set_gangs_data(self.gang_controller.get_all_gangs())
    
    def load_initial_data(self):
        """Load initial data for the application"""
        self.criminals_view.set_criminals_data(self.criminal_controller.get_all_criminals())
        
    def start(self):
        """Start the application by showing the login view"""
        return self.navigation.navigate_to('login')
        
    def close(self):
        """Close application resources"""
        self.db_connector.close()