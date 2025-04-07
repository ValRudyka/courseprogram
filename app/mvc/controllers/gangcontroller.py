from PySide6.QtCore import QObject, Signal, Slot

class GangController(QObject):
    gang_added = Signal(int)
    gang_updated = Signal(int)
    gang_deleted = Signal(int)
    operation_error = Signal(str)
    
    def __init__(self, criminal_group_model, city_model):
        super().__init__()
        self.criminal_group_model = criminal_group_model
        self.city_model = city_model
    
    @Slot(dict)
    def add_gang(self, data):
        """Add a new criminal group with provided data."""
        try:
            gang_id = self.criminal_group_model.create_criminal_group(data)
            self.gang_added.emit(gang_id)
            return gang_id
        except Exception as e:
            self.operation_error.emit(f"Error adding criminal group: {str(e)}")
            return None
    
    @Slot(int, dict)
    def update_gang(self, gang_id, data):
        """Update an existing criminal group."""
        try:
            success = self.criminal_group_model.update_criminal_group(gang_id, data)
            if success:
                self.gang_updated.emit(gang_id)
            return success
        except Exception as e:
            self.operation_error.emit(f"Error updating criminal group: {str(e)}")
            return False
    
    @Slot(int)
    def delete_gang(self, gang_id):
        """Delete a criminal group if it has no members."""
        try:
            success, message = self.criminal_group_model.delete_criminal_group(gang_id)
            if success:
                self.gang_deleted.emit(gang_id)
                return True
            else:
                self.operation_error.emit(message)
                return False
        except Exception as e:
            self.operation_error.emit(f"Error deleting criminal group: {str(e)}")
            return False
    
    def get_gang(self, gang_id):
        """Get a specific criminal group by ID."""
        try:
            return self.criminal_group_model.get_group_by_id(gang_id)
        except Exception as e:
            self.operation_error.emit(f"Error retrieving criminal group: {str(e)}")
            return None
    
    def get_all_gangs(self):
        """Get all criminal groups."""
        try:
            return self.criminal_group_model.get_all_criminal_groups()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving criminal groups: {str(e)}")
            return []
    
    def get_cities(self):
        """Get all cities for selection."""
        try:
            return self.city_model.get_all_cities()
        except Exception as e:
            self.operation_error.emit(f"Error retrieving cities: {str(e)}")
            return []
    
    def get_gang_members(self, gang_id):
        """Get all members of a specific gang."""
        try:
            return self.criminal_group_model.get_members_by_group_id(gang_id)
        except Exception as e:
            self.operation_error.emit(f"Error retrieving gang members: {str(e)}")
            return []
            
    def get_gangs_for_export(self):
        """Get complete criminal group data with all related information for export."""
        try:
            return self.criminal_group_model.get_groups_for_export()
        except Exception as e:
            self.operation_error.emit(f"Error exporting criminal groups: {str(e)}")
            return []