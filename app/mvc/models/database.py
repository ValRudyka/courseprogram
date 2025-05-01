from sqlalchemy import create_engine, text

class DatabaseConnector:    
    def __init__(self):
        self._engine = None
    
    def connect_engine(self, db_uri):
        try:
            self._engine = create_engine(db_uri)
            
            return True
            
        except Exception as e:
            return False
    @property
    def engine(self):
        return self._engine
    
    def close(self):
        if self._engine:
            self._engine.dispose()