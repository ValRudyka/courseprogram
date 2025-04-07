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
        """Get list of archived criminals."""
        try:
            archived_criminals = self.criminal_model.get_archived_criminals()
            self.criminal_loaded.emit(archived_criminals)
            return archived_criminals
        except Exception as e:
            self.operation_error.emit(f"Error retrieving archived criminals: {str(e)}")
            return []