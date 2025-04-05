from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu, QAbstractItemView
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QCursor
from .criminals_source import Ui_CriminalsWindow
from .criminals_table import CriminalTableModel
from .filterable_table_view import FilterableTableView

class CriminalsView(QMainWindow):
    add_criminal_requested = Signal()
    edit_criminal_requested = Signal(int)  
    archive_criminal_requested = Signal(int) 
    delete_criminal_requested = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_CriminalsWindow()
        self.ui.setupUi(self)
        
        self.original_table_view = self.ui.tableView
        
        self.filterable_table_view = FilterableTableView(self.ui.centralwidget)
        self.filterable_table_view.setObjectName("tableView")
        
        self.filterable_table_view.setGeometry(self.original_table_view.geometry())
        self.filterable_table_view.setSortingEnabled(True)
        
        self.ui.tableView = self.filterable_table_view
        self.original_table_view.setVisible(False)
        
        self.selected_criminal_id = None
        
        self.setup_connections()
        self.setup_context_menu()
        
        self.ui.pushButton.setText("Фільтрувати")
        self.ui.pushButton.clicked.connect(self.toggle_filters)
        
        self.ui.textEdit.setVisible(False)
        self.ui.comboBox.setVisible(False)
        self.ui.label.setVisible(False)
    
    def setup_connections(self):
        """Connect UI elements to their respective actions."""
        self.ui.pushButton_5.clicked.connect(self.on_add_criminal)
        self.ui.pushButton_3.clicked.connect(self.on_edit_criminal)
        self.ui.pushButton_2.clicked.connect(self.on_archive_criminal)
        self.ui.pushButton_4.clicked.connect(self.on_delete_criminal)
        
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
        
        context_menu.addAction(edit_action)
        context_menu.addAction(archive_action)
        context_menu.addSeparator()
        context_menu.addAction(delete_action)
        
        # Show menu
        context_menu.exec_(QCursor.pos())
    
    def toggle_filters(self):
        """Toggle visibility of filter inputs in the table header."""
        if hasattr(self.ui.tableView, 'setFilterVisible'):
            if hasattr(self.ui.tableView, 'filter_header') and hasattr(self.ui.tableView.filter_header, 'filter_visible'):
                visible = not self.ui.tableView.filter_header.filter_visible
                
                self.ui.tableView.setFilterVisible(visible)
                
                self.ui.pushButton.setText("Сховати фільтри" if visible else "Показати фільтри")
            else:
                self.ui.tableView.setFilterVisible(True)
                self.ui.pushButton.setText("Сховати фільтри")

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
    
    def on_table_clicked(self, index):
        """Handle table click to select a criminal."""
        if not index.isValid():
            return
            
        if hasattr(self.ui.tableView, 'filter_model') and self.ui.tableView.filter_model:
            source_index = self.ui.tableView.filter_model.mapToSource(index)
            source_row = source_index.row()
            
            source_model = self.ui.tableView.sourceModel()
            if source_model:
                id_index = source_model.index(source_row, 0)
                self.selected_criminal_id = int(source_model.data(id_index))
        else:
            id_index = self.ui.tableView.model().index(index.row(), 0)
            self.selected_criminal_id = int(self.ui.tableView.model().data(id_index))
    
    def set_criminals_data(self, criminals):
        """Set data for the criminals table."""
        self.full_data = criminals
        
        model = CriminalTableModel(criminals)
        
        self.ui.tableView.setModel(model)
        
        self.ui.tableView.setColumnWidth(0, 60) 
        self.ui.tableView.setColumnWidth(1, 120) 
        self.ui.tableView.setColumnWidth(2, 120) 
        self.ui.tableView.setColumnWidth(3, 120) 
        self.ui.tableView.setColumnWidth(4, 100)
        self.ui.tableView.setColumnWidth(5, 150)
        self.ui.tableView.setColumnWidth(6, 150)
        self.ui.tableView.setColumnWidth(7, 70)   
        self.ui.tableView.setColumnWidth(8, 70)  
        
        self.ui.tableView.verticalHeader().setVisible(False)
        
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.selected_criminal_id = None