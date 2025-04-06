from sqlalchemy import text

class LanguageModel:
    """Model for handling language-related database operations."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def get_all_languages(self):
        """Get all available languages for dropdown selection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT id_language, name FROM \"Languages\""))
                
                languages = []
                for row in result.fetchall():
                    languages.append({
                        "id": row[0],
                        "name": row[1]
                    })
                return languages
                
        except Exception as e:
            raise e
    
    def get_languages_for_criminal(self, criminal_id):
        """Get languages known by a specific criminal."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT l.id_language, l.name
                    FROM "Languages" l
                    JOIN "Criminals_Languages" cl ON l.id_language = cl.id_language
                    WHERE cl.id_criminal = :id
                    ORDER BY l.name
                    """),
                    {"id": criminal_id}
                )
                
                return [{"id": row[0], "name": row[1]} for row in result.fetchall()]
                
        except Exception as e:
            raise e