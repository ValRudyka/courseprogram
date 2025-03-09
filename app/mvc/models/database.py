from sqlalchemy import create_engine, text

class DatabaseConnector:    
    def __init__(self):
        self.engine = None
    
    def connect_engine(self, db_uri):
        try:
            self.engine = create_engine(db_uri)
            
            # тестування з'єднання
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