from PySide6.QtCore import QObject, Signal, Slot

class CriminalController(QObject):
    criminal_added = Signal(int)  
    criminal_updated = Signal(int) 
    criminal_archived = Signal(int) 
    criminal_deleted = Signal(int) 
    operation_error = Signal(str)
    
    def __init__(self, criminal_model):
        super().__init__()
        self.criminal_model = criminal_model
    
    @Slot(dict)
    def add_criminal(self, data):
        """Add a new criminal record with all related data."""
        try:
            criminal_id = self.criminal_model.create_criminal(data)
            self.criminal_added.emit(criminal_id)
            return criminal_id
        except Exception as e:
            self.operation_error.emit(f"Error adding criminal: {str(e)}")
            return None
    
    @Slot(int, dict)
    def update_criminal(self, criminal_id, data):
        """Update an existing criminal record."""
        try:
            success = self.criminal_model.update_criminal(criminal_id, data)
            if success:
                self.criminal_updated.emit(criminal_id)
            return success
        except Exception as e:
            self.operation_error.emit(f"Error updating criminal: {str(e)}")
            return False
    
    @Slot(int)
    def archive_criminal(self, criminal_id):
        """Archive a criminal by setting is_archived flag and creating archive record."""
        try:
            success = self.criminal_model.archive_criminal(criminal_id)
            if success:
                self.criminal_archived.emit(criminal_id)
            return success
        except Exception as e:
            self.operation_error.emit(f"Error archiving criminal: {str(e)}")
            return False
    
    @Slot(int)
    def delete_criminal(self, criminal_id):
        """Completely delete a criminal and all related records."""
        try:
            success = self.criminal_model.delete_criminal(criminal_id)
            if success:
                self.criminal_deleted.emit(criminal_id)
            return success
        except Exception as e:
            self.operation_error.emit(f"Error deleting criminal: {str(e)}")
            return False
    
    def get_criminal(self, criminal_id):
        """Get complete criminal data by ID."""
        try:
            return self.criminal_model.get_criminal_by_id(criminal_id)
        except Exception as e:
            self.operation_error.emit(f"Error retrieving criminal: {str(e)}")
            return None
    
    def get_all_criminals(self, include_archived=False):
        """Get list of all criminals."""
        try:
            return self.criminal_model.get_all_criminals(include_archived)
        except Exception as e:
            self.operation_error.emit(f"Error retrieving criminals: {str(e)}")
            return []
    
    def get_archived_criminals(self):
        """Get list of archived criminals."""
        try:
            return self.criminal_model.get_archived_criminals()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving archived criminals: {str(e)}")
            return []
    
    def get_professions(self):
        """Get all professions for selection."""
        try:
            return self.criminal_model.get_all_professions()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving professions: {str(e)}")
            return []
    
    def get_criminal_groups(self):
        """Get all criminal groups for selection."""
        try:
            return self.criminal_model.get_all_criminal_groups()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving criminal groups: {str(e)}")
            return []
    
    def get_languages(self):
        """Get all languages for selection."""
        try:
            return self.criminal_model.get_all_languages()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving languages: {str(e)}")
            return []
    
    def get_cities(self):
        """Get all cities for selection."""
        try:
            return self.criminal_model.get_all_cities()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving cities: {str(e)}")
            return []