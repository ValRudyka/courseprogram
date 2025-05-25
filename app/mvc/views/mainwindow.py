from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal, QTimer, QDateTime, QLocale, QUrl
from PySide6.QtGui import QDesktopServices
from .main_source import Ui_MainWindow
import os
import sys
import subprocess
import platform

from utils.icon_utils import icon_manager

class MainWindow(QMainWindow):
    open_criminals_requested = Signal()
    open_groups_requested = Signal()
    open_archive_requested = Signal()
    open_change_password_requested = Signal()
    open_users_requested = Signal()
    open_dashboard_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)        

        self.setup_icons()
        self.ui.pushButton_2.clicked.connect(self._on_criminals_action)
        self.ui.pushButton_3.clicked.connect(self._on_groups_action)
        self.ui.pushButton_4.clicked.connect(self._on_archive_action)
        self.ui.pushButton_6.clicked.connect(self._on_change_password_action)
        self.ui.pushButton_7.clicked.connect(self._on_users_action) 

        # Connect the instruction button to open PDF
        self.ui.pushButton.clicked.connect(self._on_instruction_action)

        self.ui.pushButton_5.setEnabled(True)
        self.ui.pushButton_5.clicked.connect(self._on_dashboard_action)
        
        self.setup_time_display()

    def setup_icons(self) -> None:
        button_icons = {
            self.ui.pushButton: "icons8-sun-64",
            self.ui.pushButton_2: "icons8-prisoner-64",
            self.ui.pushButton_3: "icons8-gang-64",
            self.ui.pushButton_4: "icons8-archive-30",
            self.ui.pushButton_5: "icons8-dashboard-64",
            self.ui.pushButton_6: "icons8-update-password-30",
            self.ui.pushButton_7: "icons8-users-30"
        }
        
        for button, icon_name in button_icons.items():
            icon_manager.set_button_icon(button, icon_name)
    
    def setup_time_display(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.ukrainian_locale = QLocale(QLocale.Ukrainian, QLocale.Ukraine)
        
        self.update_time()
    
    def update_time(self) -> None:
        now = QDateTime.currentDateTime()
        
        day_name = self.ukrainian_locale.toString(now, "dddd")
        day_number = now.toString("d")
        month_name = self.ukrainian_locale.toString(now, "MMMM")
        
        date_text = f"{day_name}, {day_number} {month_name}"
        
        time_text = now.toString("HH:mm:ss")
        
        full_text = f"{date_text}\n{time_text}"
        
        self.ui.label_2.setText(full_text)

    def _on_instruction_action(self) -> None:
        try:
            if getattr(sys, 'frozen', False):
                app_dir = os.path.dirname(sys.executable)
            else:
                current_file = os.path.abspath(__file__)
                app_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            
            pdf_path = os.path.join(app_dir, "docs", "documentation.pdf")
            
            if not os.path.exists(pdf_path):
                QMessageBox.warning(
                    self, 
                    "Файл не знайдено", 
                    f"Файл документації не знайдено за шляхом:\n{pdf_path}\n\nПереконайтеся, що файл існує в папці docs."
                )
                return
            
            success = self._open_pdf_file(pdf_path)
            
            if not success:
                QMessageBox.warning(
                    self, 
                    "Помилка відкриття файлу", 
                    "Не вдалося відкрити файл документації. Переконайтеся, що у вас встановлено програму для перегляду PDF файлів."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Помилка", 
                f"Сталася помилка при спробі відкрити документацію:\n{str(e)}"
            )
    
    def _open_pdf_file(self, file_path: str) -> bool:
        try:
            system = platform.system().lower()
            
            if system == "windows":
                os.startfile(file_path)
                return True
                
            elif system == "darwin":
                subprocess.run(["open", file_path], check=True)
                return True
                
            elif system == "linux":
                subprocess.run(["xdg-open", file_path], check=True)
                return True
                
            else:
                url = QUrl.fromLocalFile(file_path)
                return QDesktopServices.openUrl(url)
                
        except subprocess.CalledProcessError:
            try:
                url = QUrl.fromLocalFile(file_path)
                return QDesktopServices.openUrl(url)
            except Exception:
                return False
        except Exception:
            return False

    def closeEvent(self, event) -> None:
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()

    def _on_criminals_action(self) -> None:
        self.open_criminals_requested.emit()

    def _on_groups_action(self) -> None:
        self.open_groups_requested.emit()

    def _on_archive_action(self) -> None:
        self.open_archive_requested.emit()
        
    def _on_change_password_action(self) -> None:
        self.open_change_password_requested.emit()
        
    def _on_add_criminal(self) -> None:
        self.open_criminals_requested.emit()
    
    def _on_add_group(self) -> None:
        self.open_groups_requested.emit()
    
    def _on_users_action(self) -> None:
        self.open_users_requested.emit()

    def set_user_role(self, username: str) -> None:
        is_admin = (username == 'admin')
        self.ui.pushButton_7.setVisible(is_admin)

    def _on_dashboard_action(self) -> None:
        self.open_dashboard_requested.emit()