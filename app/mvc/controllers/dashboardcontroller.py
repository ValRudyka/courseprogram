from PySide6.QtCore import QObject, Signal, Slot

class DashboardController(QObject):
    dashboard_loaded = Signal()
    operation_error = Signal(str)
    
    def __init__(self, criminal_model, city_model, crime_model=None):
        super().__init__()
        self.criminal_model = criminal_model
        self.city_model = city_model
        self.crime_model = crime_model
    
    def get_dashboard_data(self):
        try:
            return self.criminal_model.get_criminals_for_export(include_archived=True)
        except Exception as e:
            self.operation_error.emit(f"Error retrieving dashboard data: {str(e)}")
            return []