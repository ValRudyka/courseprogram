from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu, QAbstractItemView
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QCursor
from .criminals_source import Ui_CriminalsWindow
from .criminals_table import CriminalTableModel

class CriminalsView(QMainWindow):
    add_criminal_requested = Signal()
    edit_criminal_requested = Signal(int)  
    archive_criminal_requested = Signal(int) 
    delete_criminal_requested = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_CriminalsWindow()
        self.ui.setupUi(self)
        
        # Selected criminal ID
        self.selected_criminal_id = None
        
        # Connect buttons
        self.setup_connections()
        
        # Set up context menu for table
        self.setup_context_menu()
    
    def setup_connections(self):
        """Connect UI elements to their respective actions."""
        # Connect main buttons
        self.ui.pushButton_5.clicked.connect(self.on_add_criminal)
        self.ui.pushButton_3.clicked.connect(self.on_edit_criminal)
        self.ui.pushButton_2.clicked.connect(self.on_archive_criminal)
        self.ui.pushButton_4.clicked.connect(self.on_delete_criminal)
        
        # Connect search button
        self.ui.pushButton.clicked.connect(self.on_search)
        
        # Connect table selection
        self.ui.tableView.clicked.connect(self.on_table_clicked)
    
    def setup_context_menu(self):
        """Create context menu for right-clicking in the table."""
        self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        """Show context menu with actions for the selected criminal."""
        if self.selected_criminal_id is None:
            return
            
        context_menu = QMenu()
        
        # Add actions
        edit_action = QAction("Редагувати", self)
        edit_action.triggered.connect(self.on_edit_criminal)
        
        archive_action = QAction("Архівувати", self)
        archive_action.triggered.connect(self.on_archive_criminal)
        
        delete_action = QAction("Видалити", self)
        delete_action.triggered.connect(self.on_delete_criminal)
        
        # Add actions to menu
        context_menu.addAction(edit_action)
        context_menu.addAction(archive_action)
        context_menu.addSeparator()
        context_menu.addAction(delete_action)
        
        # Show menu
        context_menu.exec_(QCursor.pos())
    
    def on_add_criminal(self):
        """Handle add button click."""
        self.add_criminal_requested.emit()
    
    def on_edit_criminal(self):
        """Handle edit button click."""
        if self.selected_criminal_id is None:
            QMessageBox.warning(self, "Warning", "Виберіть злочинця для редагування")
            return
        
        self.edit_criminal_requested.emit(self.selected_criminal_id)
    
    def on_archive_criminal(self):
        """Handle archive button click."""
        if self.selected_criminal_id is None:
            QMessageBox.warning(self, "Warning", "Виберіть злочинця для архівування")
            return
        
        # Confirm archive
        reply = QMessageBox.question(
            self, 
            "Підтвердження", 
            "Ви впевнені, що хочете архівувати цього злочинця?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.archive_criminal_requested.emit(self.selected_criminal_id)
    
    def on_delete_criminal(self):
        """Handle delete button click."""
        if self.selected_criminal_id is None:
            QMessageBox