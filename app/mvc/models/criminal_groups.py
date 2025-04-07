from sqlalchemy import text

class CriminalGroupModel:
    """Model for handling criminal group-related database operations."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def get_all_criminal_groups(self):
        """Get all available criminal groups for dropdown selection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                SELECT 
                    g.group_id, g.name, g.founding_date, g.number_of_members,
                    g.main_activity, c.city_name AS base_location,
                FROM "Criminal_groups" g
                LEFT JOIN "Cities" c ON g.id_base = c.id_city
                LEFT JOIN "Criminals" cr ON g.group_id = cr.id_group
                """))
                
                groups = []
                for row in result.fetchall():
                    groups.append({
                        "id": row[0],
                        "name": row[1],
                        "founding_date": row[2].strftime("%Y-%m-%d") if row[2] else None,
                        "number_of_members": row[3],
                        "main_activity": row[4],
                        "base_location": row[5],
                    })
                
                return groups
                
        except Exception as e:
            raise e
    
    def get_group_by_id(self, group_id):
        """Get information about a specific criminal group."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                SELECT 
                    g.group_id, g.name, g.founding_date, g.number_of_members,
                    g.main_activity, c.city_name AS base_location,
                FROM "Criminal_groups" g
                LEFT JOIN "Cities" c ON g.id_base = c.id_city
                LEFT JOIN "Criminals" cr ON g.group_id = cr.id_group
                WHERE g.group_id = :id
                """), {"id": group_id})
                
                row = result.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "name": row[1],
                        "founding_date": row[2].strftime("%Y-%m-%d") if row[2] else None,
                        "number_of_members": row[3],
                        "main_activity": row[4],
                        "base_location": row[5],
                    }
                return None
                
        except Exception as e:
            raise e