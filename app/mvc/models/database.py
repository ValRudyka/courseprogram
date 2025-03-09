from sqlalchemy import create_engine, text

class DatabaseConnector:
    """Manages database connections for the application"""
    
    def __init__(self):
        self.engine = None
    
    def connect(self, db_uri):
        """Connect to the PostgreSQL database"""
        try:
            self.engine = create_engine(db_uri)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            return True
            
        except Exception as e:
            return False
    
    def get_engine(self):
        return self.engine
    
    def close(self):
        if self.engine:
            self.engine.dispose()