from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu, QAbstractItemView, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QCursor
from datetime import datetime

from .gangs_source import Ui_MainWindow
from .gang_table_model import GangTableModel
from mvc.views.criminals.filterable_table_view import FilterableTableView
from utils.export_utils import export_data_to_file
from utils.icon_utils import icon_manager

class GangsView(QMainWindow):
    add_gang_requested = Signal()
    edit_gang_requested = Signal(int)
    delete_gang_requested = Signal(int)
    export_gangs_requested = Signal()
    
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_icons()
        self.original_table_view = self.ui.tableView
        
        self.filterable_table_view = FilterableTableView(self.ui.centralwidget)
        self.filterable_table_view.setObjectName("tableView")
        
        self.filterable_table_view.setGeometry(self.original_table_view.geometry())
        self.filterable_table_view.setSortingEnabled(True)
        
        self.ui.tableView = self.filterable_table_view
        self.original_table_view.setVisible(False)
        
        self.selected_gang_id = None
        
        self.setup_connections()
        self.setup_context_menu()
    
    def setup_icons(self) -> None:
        button_icons = {
            self.ui.pushButton: 'icons8-filter-50',
            self.ui.pushButton_2: 'icons8-export-file-30',
            self.ui.pushButton_3: 'icons8-update-48',
            self.ui.pushButton_4: 'icons8-delete-30',
            self.ui.pushButton_5: 'icons8-add-30'
        }

        for button, icon in button_icons.items():
            icon_manager.set_button_icon(button, icon, size=(18,18))

    def setup_connections(self) -> None:
        self.ui.pushButton_5.clicked.connect(self.on_add_gang)
        self.ui.pushButton_3.clicked.connect(self.on_edit_gang)
        self.ui.pushButton_4.clicked.connect(self.on_delete_gang)
        self.ui.pushButton.clicked.connect(self.toggle_filters)
        self.ui.pushButton_2.clicked.connect(self.on_export_gangs)
        
        self.ui.tableView.clicked.connect(self.on_table_clicked)
    
    def setup_context_menu(self) -> None:
        self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position) -> None:
        if self.selected_gang_id is None:
            return
            
        context_menu = QMenu()
        edit_action = QAction("Редагувати", self)
        edit_action.triggered.connect(self.on_edit_gang)
        
        delete_action = QAction("Видалити", self)
        delete_action.triggered.connect(self.on_delete_gang)
        
        context_menu.addAction(edit_action)
        context_menu.addSeparator()
        context_menu.addAction(delete_action)
        
        # Show menu
        context_menu.exec_(QCursor.pos())
    
    def toggle_filters(self) -> None:
        if hasattr(self.ui.tableView, 'setFilterVisible'):
            if hasattr(self.ui.tableView, 'filter_header') and hasattr(self.ui.tableView.filter_header, 'filter_visible'):
                visible = not self.ui.tableView.filter_header.filter_visible
                
                self.ui.tableView.setFilterVisible(visible)
                
                self.ui.pushButton.setText("Сховати фільтри" if visible else "Показати фільтри")
            else:
                self.ui.tableView.setFilterVisible(True)
                self.ui.pushButton.setText("Сховати фільтри")

    def on_add_gang(self) -> None:
        self.add_gang_requested.emit()
    
    def on_edit_gang(self) -> None:
        if self.selected_gang_id is None:
            QMessageBox.warning(self, "Попередження", "Виберіть угруповання для редагування")
            return
        
        self.edit_gang_requested.emit(self.selected_gang_id)
    
    def on_delete_gang(self) -> None:
        if self.selected_gang_id is None:
            QMessageBox.warning(self, "Попередження", "Виберіть угруповання для видалення")
            return
        
        reply = QMessageBox.warning(
            self, 
            "Підтвердження видалення", 
            "Ви впевнені, що хочете видалити це угруповання? Ця дія не може бути скасована.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.delete_gang_requested.emit(self.selected_gang_id)
    
    def on_table_clicked(self, index) -> None:
        if not index.isValid():
            return
            
        if hasattr(self.ui.tableView, 'filter_model') and self.ui.tableView.filter_model:
            source_index = self.ui.tableView.filter_model.mapToSource(index)
            source_row = source_index.row()
            
            source_model = self.ui.tableView.sourceModel()
            if source_model:
                id_index = source_model.index(source_row, 0)
                self.selected_gang_id = int(source_model.data(id_index))
        else:
            id_index = self.ui.tableView.model().index(index.row(), 0)
            self.selected_gang_id = int(self.ui.tableView.model().data(id_index))
    
    def set_gangs_data(self, gangs: list) -> None:
        self.full_data = gangs
        
        model = GangTableModel(gangs)
        
        self.ui.tableView.setModel(model)
        
        self.ui.tableView.setColumnWidth(0, 60)  
        self.ui.tableView.setColumnWidth(1, 150) 
        self.ui.tableView.setColumnWidth(2, 120) 
        self.ui.tableView.setColumnWidth(3, 100)
        self.ui.tableView.setColumnWidth(4, 200) 
        self.ui.tableView.setColumnWidth(5, 170) 
        self.ui.tableView.setColumnWidth(6, 80)
        
        self.ui.tableView.verticalHeader().setVisible(False)
        
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.selected_gang_id = None
        
    def on_export_gangs(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Експорт даних")
        layout = QVBoxLayout(dialog)
        
        label = QLabel("Експорт даних угруповань:", dialog)
        layout.addWidget(label)
        
        buttons_layout = QHBoxLayout()
        export_button = QPushButton("Експортувати", dialog)
        cancel_button = QPushButton("Скасувати", dialog)
        
        buttons_layout.addWidget(export_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
        export_button.clicked.connect(lambda: self._perform_export(dialog))
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.setMinimumWidth(300)
        dialog.exec_()
    
    def _perform_export(self, dialog) -> None:
        dialog.accept()
        self.export_gangs_requested.emit()
        
    def export_gangs_data(self, data: list) -> None:
        if not data:
            QMessageBox.warning(self, "Експорт", "Немає даних для експорту.")
            return
        
        export_data_to_file(data, self, f"угруповання_{datetime.now().strftime('%Y%m%d')}")
    
    def closeEvent(self, event) -> None:
        event.accept()