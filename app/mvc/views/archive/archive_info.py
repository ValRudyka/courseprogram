from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu, QAbstractItemView
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QCursor

from .archive_source import Ui_MainWindow
from .archive_table_model import ArchiveTableModel
from mvc.views.criminals.filterable_table_view import FilterableTableView

class ArchiveView(QMainWindow):
    delete_archived_criminal_requested = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setup_table_view()
        
        self.selected_criminal_id = None
        
        self.setup_connections()
        self.setup_context_menu()
    
    def setup_table_view(self):
        """Replace standard table with filterable table view."""
        self.filterable_table_view = FilterableTableView(self.ui.centralwidget)
        self.filterable_table_view.setObjectName("tableWidget")
        
        self.filterable_table_view.setGeometry(self.ui.tableWidget.geometry())
        self.filterable_table_view.setSortingEnabled(True)
        
        self.original_table_widget = self.ui.tableWidget
        self.ui.tableWidget = self.filterable_table_view
        self.original_table_widget.setVisible(False)
    
    def setup_connections(self):
        """Connect UI elements to their respective actions."""
        self.ui.pushButton_4.clicked.connect(self.on_delete_criminal)
        self.ui.pushButton_6.clicked.connect(self.toggle_filters)
        
        self.ui.tableWidget.clicked.connect(self.on_table_clicked)
    
    def setup_context_menu(self):
        """Create context menu for right-clicking in the table."""
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        """Show context menu with actions for the selected criminal."""
        if self.selected_criminal_id is None:
            return
            
        context_menu = QMenu()
        
        delete_action = QAction("Видалити назавжди", self)
        delete_action.triggered.connect(self.on_delete_criminal)
        
        context_menu.addAction(delete_action)
        
        context_menu.exec_(QCursor.pos())
    
    def toggle_filters(self):
        """Toggle visibility of filter inputs in the table header."""
        if hasattr(self.ui.tableWidget, 'setFilterVisible'):
            if hasattr(self.ui.tableWidget, 'filter_header') and hasattr(self.ui.tableWidget.filter_header, 'filter_visible'):
                visible = not self.ui.tableWidget.filter_header.filter_visible
                
                self.ui.tableWidget.setFilterVisible(visible)
                
                self.ui.pushButton_6.setText("Сховати фільтри" if visible else "Показати фільтри")
            else:
                self.ui.tableWidget.setFilterVisible(True)
                self.ui.pushButton_6.setText("Сховати фільтри")
    
    def on_table_clicked(self, index):
        """Handle table click to select a criminal."""
        if not index.isValid():
            return
            
        if hasattr(self.ui.tableWidget, 'filter_model') and self.ui.tableWidget.filter_model:
            source_index = self.ui.tableWidget.filter_model.mapToSource(index)
            source_row = source_index.row()
            
            source_model = self.ui.tableWidget.sourceModel()
            if source_model:
                id_index = source_model.index(source_row, 0)
                self.selected_criminal_id = int(source_model.data(id_index))
        else:
            model = self.ui.tableWidget.model()
            if model:
                id_index = model.index(index.row(), 0)
                self.selected_criminal_id = int(model.data(id_index))
    
    def on_delete_criminal(self):
        """Handle delete button click."""
        if self.selected_criminal_id is None:
            QMessageBox.warning(self, "Попередження", "Виберіть злочинця для видалення з архіву")
            return
        
        reply = QMessageBox.warning(
            self, 
            "Підтвердження видалення", 
            "Ви впевнені, що хочете ПОВНІСТЮ видалити цього злочинця? Ця дія не може бути скасована.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.delete_archived_criminal_requested.emit(self.selected_criminal_id)
    
    def set_archive_data(self, criminals):
        """Set data for the archive table."""
        self.archive_data = criminals
        
        model = ArchiveTableModel(criminals)
        
        self.ui.tableWidget.setModel(model)
        
        self.ui.tableWidget.setColumnWidth(0, 60)   
        self.ui.tableWidget.setColumnWidth(1, 120) 
        self.ui.tableWidget.setColumnWidth(2, 120) 
        self.ui.tableWidget.setColumnWidth(3, 100)  
        self.ui.tableWidget.setColumnWidth(4, 150)  
        self.ui.tableWidget.setColumnWidth(5, 150)
        self.ui.tableWidget.setColumnWidth(6, 120)  
        self.ui.tableWidget.setColumnWidth(7, 70)   
        self.ui.tableWidget.setColumnWidth(8, 70)   
        self.ui.tableWidget.setColumnWidth(9, 150)  
        self.ui.tableWidget.setColumnWidth(10, 120) 
        
        self.ui.tableWidget.verticalHeader().setVisible(False)
        
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.selected_criminal_id = None