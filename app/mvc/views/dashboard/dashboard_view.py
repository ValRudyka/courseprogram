from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings

from .dashboard_source import Ui_DashboardWindow
from .bokeh_dashboard import create_bokeh_dashboard

class DashboardView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DashboardWindow()
        self.ui.setupUi(self)
        
        self.dashboard_layout = QVBoxLayout(self.ui.dashboard_container)
        self.dashboard_layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        
        self.dashboard_layout.addWidget(self.web_view)
        
        self.setWindowTitle("Дашборд злочинців")
    
    def set_dashboard_data(self, data):
        """Set data for the dashboard and render it."""
        if not data:
            self._show_no_data_message()
            return
        
        dashboard_html = create_bokeh_dashboard(data)
        
        self.web_view.setHtml(dashboard_html)
    
    def _show_no_data_message(self):
        """Show a message when no data is available."""
        self.web_view.setHtml("""
        <html>
        <body style="display: flex; justify-content: center; align-items: center; height: 100%; font-family: Arial, sans-serif;">
            <h2>Немає даних для відображення на дашборді</h2>
        </body>
        </html>
        """)