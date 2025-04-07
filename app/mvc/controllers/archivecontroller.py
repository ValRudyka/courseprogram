from PySide6.QtCore import QObject, Signal, Slot

class ArchiveController(QObject):
    criminal_deleted = Signal(int)
    criminal_loaded = Signal(list)
    operation_error = Signal(str)
    
    def __init__(self, criminal_model):
        super().__init__()
        self.criminal_model = criminal_model
    
    @Slot(int)
    def delete_archived_criminal(self, criminal_id):
        """Completely delete a criminal from archives and database."""
        try:
            success = self.criminal_model.delete_criminal(criminal_id)
            if success:
                self.criminal_deleted.emit(criminal_id)
                return True
            return False
        except Exception as e:
            self.operation_error.emit(f"Error deleting archived criminal: {str(e)}")
            return False
    
    def get_archived_criminals(self):
        """Get list of archived criminals with complete information."""
        try:
            archived_criminals = self.criminal_model.get_archived_criminals()
            
            enhanced_data = []
            for criminal in archived_criminals:
                criminal_id = criminal.get("id_criminal")
                full_data = self.criminal_model.get_criminal_by_id(criminal_id)
                
                if full_data:
                    archive_date = criminal.get("archive_date")
                    full_data["archive_date"] = archive_date
                    
                    enhanced_data.append(full_data)
                else:
                    enhanced_data.append(criminal)
            
            self.criminal_loaded.emit(enhanced_data)
            return enhanced_data
        except Exception as e:
            self.operation_error.emit(f"Error retrieving archived criminals: {str(e)}")
            return []