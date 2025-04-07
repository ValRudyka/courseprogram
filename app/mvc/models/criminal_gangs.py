from sqlalchemy import text
from datetime import datetime

class CriminalGroupModel:
    """Model for handling criminal group-related database operations."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def get_next_id(self, table_name, id_column):
        """Get the next available ID for a given table."""
        try:
            with self.engine.connect() as conn:
                query = f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM \"{table_name}\""
                result = conn.execute(text(query))
                return result.scalar()
        except Exception as e:
            raise e
    
    def get_all_criminal_groups(self):
        """Get all available criminal groups for display and selection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                WITH leader_info AS (
                    SELECT 
                        c.id_group,
                        CONCAT(c.first_name,' ',c.last_name) AS leader_name
                    FROM "Criminals" c
                    WHERE c.role = 'лідер' AND c.is_archived = FALSE
                )
                SELECT 
                    g.group_id, g.name, g.founding_date, g.number_of_members,
                    g.main_activity, c.city_name AS base_location, c.id_city AS base_id,
                    l.leader_name,
                    COUNT(cr.id_criminal) AS active_members
                FROM "Criminal_groups" g
                LEFT JOIN "Cities" c ON g.id_base = c.id_city
                LEFT JOIN "Criminals" cr ON g.group_id = cr.id_group AND cr.is_archived = FALSE
                LEFT JOIN leader_info l ON g.group_id = l.id_group
                GROUP BY g.group_id, c.city_name, c.id_city, l.leader_name
                ORDER BY g.name
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
                        "base_id": row[6],
                        "leader_name": row[7] or 'Невідомо',
                        "active_members": row[8]
                    })
                
                return groups
                
        except Exception as e:
            raise e
    
    def get_group_by_id(self, group_id):
        """Get complete information about a specific criminal group."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                SELECT 
                    g.group_id, g.name, g.founding_date, g.number_of_members,
                    g.main_activity, g.status, g.id_base,
                    c.city_name AS base_location, c.id_city AS base_id,
                    COUNT(cr.id_criminal) AS active_members
                FROM "Criminal_groups" g
                LEFT JOIN "Cities" c ON g.id_base = c.id_city
                LEFT JOIN "Criminals" cr ON g.group_id = cr.id_group AND cr.is_archived = FALSE
                WHERE g.group_id = :id
                GROUP BY g.group_id, c.city_name, c.id_city
                """), {"id": group_id})
                
                row = result.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "name": row[1],
                        "founding_date": row[2].strftime("%Y-%m-%d") if row[2] else None,
                        "number_of_members": row[3],
                        "main_activity": row[4],
                        "status": row[5],
                        "base_id": row[6],
                        "base_location": row[7],
                        "active_members": row[9]
                    }
                return None
                
        except Exception as e:
            raise e
    
    def create_criminal_group(self, data):
        """Create a new criminal group with the provided data."""
        try:
            with self.engine.connect() as conn:
                transaction = conn.begin()
                
                next_id = self.get_next_id("Criminal_groups", "group_id")
                
                result = conn.execute(
                    text("""
                    INSERT INTO "Criminal_groups" (
                        group_id, name, founding_date, number_of_members,
                        main_activity, status, id_base
                    ) 
                    VALUES (
                        :group_id, :name, :founding_date, :number_of_members,
                        :main_activity, :status, :id_base
                    )
                    RETURNING group_id
                    """), 
                    {
                        "group_id": next_id,
                        "name": data.get("name"),
                        "founding_date": data.get("founding_date"),
                        "number_of_members": data.get("number_of_members"),
                        "main_activity": data.get("main_activity"),
                        "status": data.get("status", "Active"),
                        "id_base": data.get("base_id")
                    }
                )
                group_id = result.fetchone()[0]
                
                transaction.commit()
                return group_id
                
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def update_criminal_group(self, group_id, data):
        """Update an existing criminal group with the provided data."""
        try:
            with self.engine.connect() as conn:
                transaction = conn.begin()
                
                conn.execute(
                    text("""
                    UPDATE "Criminal_groups" SET
                        name = :name,
                        founding_date = :founding_date,
                        number_of_members = :number_of_members,
                        main_activity = :main_activity,
                        status = :status,
                        id_base = :id_base
                    WHERE group_id = :group_id
                    """), 
                    {
                        "group_id": group_id,
                        "name": data.get("name"),
                        "founding_date": data.get("founding_date"),
                        "number_of_members": data.get("number_of_members"),
                        "main_activity": data.get("main_activity"),
                        "status": data.get("status", "Active"),
                        "id_base": data.get("base_id")
                    }
                )
                
                transaction.commit()
                return True
                
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def delete_criminal_group(self, group_id):
        """Delete a criminal group (checks if there are still criminals in the group first)."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT COUNT(*) FROM \"Criminals\" WHERE id_group = :id"),
                    {"id": group_id}
                )
                count = result.scalar()
                
                if count > 0:
                    return False, f"Неможливо видалити угрупування, оскільки до нього належать {count} злочинців"
                
                transaction = conn.begin()
                
                conn.execute(
                    text("DELETE FROM \"Criminal_groups\" WHERE group_id = :id"),
                    {"id": group_id}
                )
                
                transaction.commit()
                return True, ""
                
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def get_members_by_group_id(self, group_id):
        """Get all active criminals that belong to a specific group."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT 
                        c.id_criminal, c.first_name, c.last_name, c.nickname, c.role,
                        p.height, p.weight
                    FROM "Criminals" c
                    LEFT JOIN "Physical_characteristics" p ON c.id_criminal = p.id_criminal
                    WHERE c.id_group = :group_id AND c.is_archived = FALSE
                    ORDER BY c.last_name, c.first_name
                    """),
                    {"group_id": group_id}
                )
                
                members = []
                for row in result.fetchall():
                    members.append({
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "nickname": row[3],
                        "role": row[4],
                        "height": row[5],
                        "weight": row[6]
                    })
                
                return members
                
        except Exception as e:
            raise e
    
    def get_groups_for_export(self):
        """Get complete criminal group data with all related information for export, including leader information."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    WITH leader_info AS (
                        SELECT 
                            c.id_group,
                            CONCAT(c.first_name,' ',c.last_name) AS leader_name
                        FROM "Criminals" c
                        WHERE c.role = 'лідер' AND c.is_archived = FALSE
                    )
                    SELECT 
                        g.group_id, g.name, g.founding_date, g.number_of_members,
                        g.main_activity, g.status, c.city_name AS base_location,
                        l.leader_name,
                        COUNT(cr.id_criminal) AS active_members
                    FROM "Criminal_groups" g
                    LEFT JOIN "Cities" c ON g.id_base = c.id_city
                    LEFT JOIN "Criminals" cr ON g.group_id = cr.id_group AND cr.is_archived = FALSE
                    LEFT JOIN leader_info l ON g.group_id = l.id_group
                    GROUP BY g.group_id, c.city_name, l.leader_name
                    ORDER BY g.name
                    """)
                )
                
                groups_data = []
                for row in result:
                    data = {
                        "ID": row[0],
                        "Назва": row[1],
                        "Дата заснування": row[2].strftime("%Y-%m-%d") if row[2] else "",
                        "Кількість членів": row[3] or 0,
                        "Основна діяльність": row[4] or "",
                        "Статус": row[5] or "",
                        "Місце бази": row[6] or "",
                        "Лідер": row[7] or "Невідомо",
                        "Активних членів": row[8] or 0
                    }
                    groups_data.append(data)
                
                return groups_data
                
        except Exception as e:
            raise e