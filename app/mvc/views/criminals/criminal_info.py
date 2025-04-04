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
            QMessageBox.warning(self, "Warning", "Виберіть злочинця для видалення")
            return
        
        reply = QMessageBox.warning(
            self, 
            "Підтвердження видалення", 
            "Ви впевнені, що хочете видалити цього злочинця? Ця дія не може бути скасована.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.delete_criminal_requested.emit(self.selected_criminal_id)
    
    def on_search(self):
        """Handle search button click."""
        # Get search field and text
        search_field = self.ui.comboBox.currentText()
        search_text = self.ui.textEdit.toPlainText().strip()
        
        if not search_text:
            # If search text is empty, clear any filtering
            self.set_criminals_data(self.full_data)
            return
        
        # Map search field to model column
        field_map = {
            "Ім'я": "first_name",
            "Прізвище": "last_name",
            "Кличка": "nickname",
            "Місце народження": "birth_place",
            "Місце проживання": "residence"
        }
        
        if search_field in field_map:
            field_key = field_map[search_field]
            # Filter the data
            filtered_data = [
                criminal for criminal in self.full_data
                if search_text.lower() in str(criminal.get(field_key, "")).lower()
            ]
            # Update the table with filtered data
            self.ui.tableView.model().update_data(filtered_data)
        else:
            # If field not recognized, do nothing
            pass
    
    def on_table_clicked(self, index):
        """Handle table click to select a criminal."""
        if not index.isValid():
            return
            
        # Get the ID from the first column
        id_index = self.ui.tableView.model().index(index.row(), 0)
        self.selected_criminal_id = int(self.ui.tableView.model().data(id_index))
    
    def set_criminals_data(self, criminals):
        """Set data for the criminals table."""
        # Store the full data for filtering
        self.full_data = criminals
        
        # Create and set table model
        model = CriminalTableModel(criminals)
        self.ui.tableView.setModel(model)
        
        # Enable sorting
        self.ui.tableView.setSortingEnabled(True)
        
        # Set column widths
        self.ui.tableView.setColumnWidth(0, 50)   # ID
        self.ui.tableView.setColumnWidth(1, 120)  # First name
        self.ui.tableView.setColumnWidth(2, 120)  # Last name
        self.ui.tableView.setColumnWidth(3, 120)  # Nickname
        self.ui.tableView.setColumnWidth(4, 100)  # Birth date
        self.ui.tableView.setColumnWidth(5, 150)  # Birth place
        self.ui.tableView.setColumnWidth(6, 150)  # Residence
        self.ui.tableView.setColumnWidth(7, 70)   # Height
        self.ui.tableView.setColumnWidth(8, 70)   # Weight
        
        # Hide vertical header
        self.ui.tableView.verticalHeader().setVisible(False)
        
        # Set selection behavior
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Clear selection
        self.selected_criminal_id = None