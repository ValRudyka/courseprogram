from sqlalchemy import text

class ProfessionModel:
    """Model for handling profession-related database operations."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def get_all_professions(self):
        """Get all available professions for dropdown selection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT id_profession, profession_name FROM \"Professions\""))
                
                professions = []
                for row in result.fetchall():
                    professions.append({
                        "id": row[0],
                        "name": row[1]
                    })
                
                return professions
                
        except Exception as e:
            raise e
    
    def get_professions_for_criminal(self, criminal_id):
        """Get professions of a specific criminal."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT p.id_profession, p.profession_name
                    FROM "Professions" p
                    JOIN "Criminals_Professions" cp ON p.id_profession = cp.id_profession
                    WHERE cp.id_criminal = :id
                    ORDER BY p.profession_name
                    """),
                    {"id": criminal_id}
                )
                
                return [{"id": row[0], "name": row[1]} for row in result.fetchall()]
                
        except Exception as e:
            raise e