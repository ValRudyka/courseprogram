from sqlalchemy import text
from datetime import datetime

class CriminalModel:
    def __init__(self, engine):
        self.engine = engine
    
    def get_next_id(self, table_name, id_column):
        try:
            with self.engine.connect() as conn:
                query = f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM \"{table_name}\""
                result = conn.execute(text(query))
                return result.scalar()
        except Exception as e:
            raise e

    def create_criminal(self, data):
        try:
            with self.engine.connect() as conn:
                transaction = conn.begin()
                
                next_id = self.get_next_id("Criminals", "id_criminal")
                
                result = conn.execute(
                    text("""
                    INSERT INTO "Criminals" (
                        id_criminal, first_name, last_name, nickname, 
                        place_of_birth_id, date_of_birth, last_live_place_id, 
                        is_archived
                    ) 
                    VALUES (
                        :id_criminal, :first_name, :last_name, :nickname, 
                        :birth_place_id, :birth_date, :last_residence_id, 
                        FALSE
                    )
                    RETURNING id_criminal
                    """), 
                    {
                        "id_criminal": next_id,
                        "first_name": data.get("first_name"),
                        "last_name": data.get("last_name"),
                        "nickname": data.get("nickname", ""),
                        "birth_place_id": data.get("birth_place_id"),
                        "birth_date": data.get("birth_date"),
                        "last_residence_id": data.get("last_residence_id")
                    }
                )
                
                criminal_id = result.fetchone()[0]
                
                next_char_id = self.get_next_id("Physical_characteristics", "id_characteristic")

                conn.execute(
                    text("""
                    INSERT INTO "Physical_characteristics" (
                        id_characteristic, id_criminal, height, weight, 
                        hair_color, eye_color, distinguishing_features
                    ) 
                    VALUES (
                        :id_characteristic, :criminal_id, :height, :weight, 
                        :hair_color, :eye_color, :features
                    )
                    """), 
                    {
                        "id_characteristic": next_char_id,
                        "criminal_id": criminal_id,
                        "height": data.get("height"),
                        "weight": data.get("weight"),
                        "hair_color": data.get("hair_color"),
                        "eye_color": data.get("eye_color"),
                        "features": data.get("distinguishing_features")
                    }
                )
                
                if data.get("last_case"):
                    next_crime_id = self.get_next_id("Crimes", "id_crime")

                    conn.execute(
                        text("""
                        INSERT INTO "Crimes" (
                            id_crime, crime_name, commitment_date, id_location, 
                            court_sentence, id_criminal
                        ) 
                        VALUES (
                            :id_crime, :crime_name, :date, :location_id,
                            :court_sentence, :criminal_id
                        )
                        """), 
                        {
                            "id_crime": next_crime_id,
                            "crime_name": data.get("last_case"),
                            "date": data.get("last_case_date"),
                            "location_id": data.get("last_case_location_id"),
                            "court_sentence": data.get("court_sentence", 1),
                            "criminal_id": criminal_id
                        }
                    )
                
                for profession_id in data.get("profession_ids", []):
                    conn.execute(
                        text("""
                        INSERT INTO "Criminals_Professions" (
                            id_criminal, id_profession
                        ) 
                        VALUES (:criminal_id, :profession_id)
                        """),
                        {
                            "criminal_id": criminal_id,
                            "profession_id": profession_id
                        }
                    )
                
                for group_id in data.get("group_ids", []):
                    conn.execute(
                        text("""
                        INSERT INTO "Criminals_Criminal_groups" (
                           id_criminal, id_group
                        ) 
                        VALUES (:criminal_id, :group_id)
                        """),
                        {
                            "criminal_id": criminal_id,
                            "group_id": group_id
                        }
                    )
                
                for language_id in data.get("language_ids", []):
                    next_language_id = self.get_next_id("Criminals_Languages", "id")
                    print(next_language_id)

                    conn.execute(
                        text("""
                        INSERT INTO "Criminals_Languages" (
                            id, id_criminal, id_language
                        ) 
                        VALUES (:id, :criminal_id, :language_id)
                        """),
                        {
                            "id": next_language_id,
                            "criminal_id": criminal_id,
                            "language_id": language_id
                        }
                    )
                
                transaction.commit()
                return criminal_id

        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def update_criminal(self, criminal_id, data):
        try:
            with self.engine.connect() as conn:
                transaction = conn.begin()
                
                conn.execute(
                    text("""
                    UPDATE "Criminals" SET
                        first_name = :first_name,
                        last_name = :last_name,
                        nickname = :nickname,
                        place_of_birth_id = :birth_place_id,
                        date_of_birth = :birth_date,
                        last_live_place_id = :last_residence_id
                    WHERE id_criminal = :criminal_id
                    """), 
                    {
                        "criminal_id": criminal_id,
                        "first_name": data.get("first_name"),
                        "last_name": data.get("last_name"),
                        "nickname": data.get("nickname"),
                        "birth_place_id": data.get("birth_place_id"),
                        "birth_date": data.get("birth_date"),
                        "last_residence_id": data.get("last_residence_id")
                    }
                )
                
                conn.execute(
                    text("""
                    UPDATE "Physical_characteristics" SET
                        height = :height,
                        weight = :weight,
                        hair_color = :hair_color,
                        eye_color = :eye_color,
                        distinguishing_features = :features
                    WHERE id_criminal = :criminal_id
                    """), 
                    {
                        "criminal_id": criminal_id,
                        "height": data.get("height"),
                        "weight": data.get("weight"),
                        "hair_color": data.get("hair_color"),
                        "eye_color": data.get("eye_color"),
                        "features": data.get("distinguishing_features")
                    }
                )
                
                conn.execute(
                    text("""
                    DELETE FROM "Criminals_Professions"
                    WHERE id_criminal = :criminal_id
                    """),
                    {"criminal_id": criminal_id}
                )
                
                for profession_id in data.get("profession_ids", []):
                    conn.execute(
                        text("""
                        INSERT INTO "Criminals_Professions" (
                            id_criminal, id_profession
                        ) 
                        VALUES (:criminal_id, :profession_id)
                        """),
                        {
                            "criminal_id": criminal_id,
                            "profession_id": profession_id
                        }
                    )
                
                conn.execute(
                    text("""
                    DELETE FROM "Criminals_Criminal_groups"
                    WHERE id_criminal = :criminal_id
                    """),
                    {"criminal_id": criminal_id}
                )
                
                for group_id in data.get("group_ids", []):
                    conn.execute(
                        text("""
                        INSERT INTO "Criminals_Criminal_groups" (
                            id_criminal, group_id
                        ) 
                        VALUES (:criminal_id, :group_id)
                        """),
                        {
                            "criminal_id": criminal_id,
                            "group_id": group_id
                        }
                    )
                
                conn.execute(
                    text("""
                    DELETE FROM "Criminals_Languages"
                    WHERE id_criminal = :criminal_id
                    """),
                    {"criminal_id": criminal_id}
                )
                
                for language_id in data.get("language_ids", []):
                    conn.execute(
                        text("""
                        INSERT INTO "Criminals_Languages" (
                            id_criminal, id_language
                        ) 
                        VALUES (:criminal_id, :language_id)
                        """),
                        {
                            "criminal_id": criminal_id,
                            "language_id": language_id
                        }
                    )
                
                if data.get("last_case"):
                    next_crime_id = self.get_next_id("Crimes", "id_crime")

                    conn.execute(
                        text("""
                        INSERT INTO "Crimes" (
                            id_crime, crime_name, commitment_date, id_location,
                            court_sentence, id_criminal
                        ) 
                        VALUES (
                            :id_crime, :crime_name, :date, :location_id,
                            :court_sentence, :criminal_id
                        )
                        """), 
                        {
                            "crime_name": data.get("last_case"),
                            "date": data.get("last_case_date"),
                            "location_id": data.get("last_case_location_id"),
                            "court_sentence": 1,
                            "criminal_id": criminal_id,
                            "id_crime": next_crime_id,
                        }
                    )
                
                transaction.commit()
                return True
                
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def archive_criminal(self, criminal_id):
        try:
            with self.engine.connect() as conn:
                transaction = conn.begin()
                
                # Update is_archived flag
                conn.execute(
                    text("""
                    UPDATE "Criminals" SET is_archived = TRUE
                    WHERE id_criminal = :criminal_id
                    """), 
                    {"criminal_id": criminal_id}
                )
                
                conn.execute(
                    text("""
                    INSERT INTO "Archive" (id_criminal, archive_date)
                    VALUES (:criminal_id, :archive_date)
                    """),
                    {
                        "criminal_id": criminal_id,
                        "archive_date": datetime.now().date()
                    }
                )
                
                transaction.commit()
                return True
                
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def delete_criminal(self, criminal_id):
        """Delete a criminal record completely from the database, removing all related records."""
        try:
            with self.engine.connect() as conn:
                transaction = conn.begin()
                
                conn.execute(
                    text("DELETE FROM \"Criminals_Languages\" WHERE Criminals_id_criminal = :id"),
                    {"id": criminal_id}
                )
                conn.execute(
                    text("DELETE FROM \"Criminals_Professions\" WHERE Criminals_id_criminal = :id"),
                    {"id": criminal_id}
                )
                conn.execute(
                    text("DELETE FROM \"Criminals_Criminal_groups\" WHERE Criminals_id_criminal = :id"),
                    {"id": criminal_id}
                )
                
                conn.execute(
                    text("UPDATE \"Criminal_groups\" SET id_leader = NULL WHERE id_leader = :id"),
                    {"id": criminal_id}
                )
                
                conn.execute(
                    text("DELETE FROM \"Physical_characteristics\" WHERE id_criminal = :id"),
                    {"id": criminal_id}
                )
                
                conn.execute(
                    text("DELETE FROM \"Crimes\" WHERE id_criminal = :id"),
                    {"id": criminal_id}
                )
                
                conn.execute(
                    text("DELETE FROM \"Archive\" WHERE id_criminal = :id"),
                    {"id": criminal_id}
                )
                
                conn.execute(
                    text("DELETE FROM \"Criminals\" WHERE id_criminal = :id"),
                    {"id": criminal_id}
                )
                
                transaction.commit()
                return True
                
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
    
    def get_criminal_by_id(self, criminal_id):
        """Get complete criminal data including all related information by ID."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT 
                        c.id_criminal, c.first_name, c.last_name, c.nickname,
                        c.place_of_birth_id, c.date_of_birth, c.last_live_place_id, c.is_archived,
                        p.height, p.weight, p.hair_color, p.eye_color, p.distinguishing_features,
                        bp.city_name as birth_place, lp.city_name as last_place
                    FROM "Criminals" c
                    JOIN "Physical_characteristics" p ON c.id_criminal = p.id_criminal
                    LEFT JOIN "Cities" bp ON c.place_of_birth_id = bp.id_city
                    LEFT JOIN "Cities" lp ON c.last_live_place_id = lp.id_city
                    WHERE c.id_criminal = :id
                    """),
                    {"id": criminal_id}
                )
                
                row = result.fetchone()
                if not row:
                    return None
                
                criminal_data = {
                    "id_criminal": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "nickname": row[3],
                    "place_of_birth_id": row[4],
                    "date_of_birth": row[5].strftime("%Y-%m-%d") if row[5] else None,
                    "last_live_place_id": row[6],
                    "is_archived": row[7],
                    "height": row[8],
                    "weight": row[9],
                    "hair_color": row[10],
                    "eye_color": row[11],
                    "distinguishing_features": row[12],
                    "birth_place_name": row[13],
                    "last_place_name": row[14]
                }
                
                crime_result = conn.execute(
                    text("""
                    SELECT 
                        crime_name, commitment_date, id_location, court_sentence,
                        c.city_name as location_name
                    FROM "Crimes" cr
                    LEFT JOIN "Cities" c ON cr.id_location = c.id_city
                    WHERE cr.id_criminal = :id
                    ORDER BY cr.commitment_date DESC
                    LIMIT 1
                    """),
                    {"id": criminal_id}
                )
                
                crime_row = crime_result.fetchone()
                if crime_row:
                    criminal_data.update({
                        "last_case": crime_row[0],
                        "last_case_date": crime_row[1].strftime("%Y-%m-%d") if crime_row[1] else None,
                        "last_case_location_id": crime_row[2],
                        "court_sentence": crime_row[3],
                        "last_case_location_name": crime_row[4]
                    })
                
                prof_result = conn.execute(
                    text("""
                    SELECT p.id_profession, p.profession_name
                    FROM "Professions" p
                    JOIN "Criminals_Professions" cp ON p.id_profession = cp.id_profession
                    WHERE cp.id_criminal = :id
                    """),
                    {"id": criminal_id}
                )
                
                criminal_data["professions"] = [
                    {"id": row[0], "name": row[1]} for row in prof_result.fetchall()
                ]
                
                group_result = conn.execute(
                    text("""
                    SELECT g.group_id, g.name
                    FROM "Criminal_groups" g
                    JOIN "Criminals_Criminal_groups" cg ON g.group_id = cg.id_group
                    WHERE cg.id_criminal = :id
                    """),
                    {"id": criminal_id}
                )
                
                criminal_data["groups"] = [
                    {"id": row[0], "name": row[1]} for row in group_result.fetchall()
                ]
                
                lang_result = conn.execute(
                    text("""
                    SELECT l.id_language, l.name
                    FROM "Languages" l
                    JOIN "Criminals_Languages" cl ON l.id_language = cl.id_language
                    WHERE cl.id_criminal = :id
                    """),
                    {"id": criminal_id}
                )
                
                criminal_data["languages"] = [
                    {"id": row[0], "name": row[1]} for row in lang_result.fetchall()
                ]
                
                return criminal_data
                
        except Exception as e:
            raise e
    
    def get_all_criminals(self, include_archived=False):
        """Get a list of all criminals with basic information for display in a table."""
        try:
            with self.engine.connect() as conn:
                query = """
                SELECT 
                    c.id_criminal, c.first_name, c.last_name, c.nickname, c.is_archived,
                    bp.city_name AS birth_place, lp.city_name AS residence,
                    c.date_of_birth, pc.height, pc.weight
                FROM "Criminals" c
                LEFT JOIN "Cities" bp ON c.place_of_birth_id = bp.id_city
                LEFT JOIN "Cities" lp ON c.last_live_place_id = lp.id_city
                LEFT JOIN "Physical_characteristics" pc ON c.id_criminal = pc.id_criminal
                """
                
                if not include_archived:
                    query += " WHERE c.is_archived = FALSE"
                
                result = conn.execute(text(query))
                
                criminals = []
                for row in result.fetchall():
                    criminals.append({
                        "id_criminal": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "nickname": row[3],
                        "is_archived": row[4],
                        "birth_place": row[5],
                        "residence": row[6],
                        "date_of_birth": row[7].strftime("%Y-%m-%d") if row[7] else None,
                        "height": row[8],
                        "weight": row[9]
                    })
                
                return criminals
                
        except Exception as e:
            raise e
    
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
    
    def get_all_criminal_groups(self):
        """Get all available criminal groups for dropdown selection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                SELECT 
                    g.group_id, g.name, g.founding_date, g.number_of_members,
                    g.main_activity, c.city_name AS base_location,
                    CONCAT(cr.first_name, ' ', cr.last_name) AS leader_name
                FROM "Criminal_groups" g
                LEFT JOIN "Cities" c ON g.id_base = c.id_city
                LEFT JOIN "Criminals" cr ON g.id_leader = cr.id_criminal
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
                        "leader_name": row[6]
                    })
                
                return groups
                
        except Exception as e:
            raise e
    
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
    
    def get_all_cities(self):
        """Get all available cities with country information for dropdown selection."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT c.id_city, c.city_name, co.country_name
                    FROM "Cities" c
                    JOIN "Countries" co ON c.id_country = co.id_country
                    ORDER BY co.country_name, c.city_name
                    """)
                )
                
                cities = []
                for row in result.fetchall():
                    cities.append({
                        "id": row[0],
                        "name": row[1],
                        "country": row[2],
                        "display_name": f"{row[1]}, {row[2]}"
                    })
                
                return cities
                
        except Exception as e:
            raise e
    
    def get_archived_criminals(self):
        """Get list of archived criminals with archive date."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT 
                        c.id_criminal, c.first_name, c.last_name, c.nickname,
                        a.archive_date, bp.city_name AS birth_place
                    FROM "Criminals" c
                    JOIN "Archive" a ON c.id_criminal = a.id_criminal
                    LEFT JOIN "Cities" bp ON c.place_of_birth_id = bp.id_city
                    WHERE c.is_archived = TRUE
                    ORDER BY a.archive_date DESC
                    """)
                )
                
                archived = []
                for row in result.fetchall():
                    archived.append({
                        "id_criminal": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "nickname": row[3],
                        "archive_date": row[4].strftime("%Y-%m-%d") if row[4] else None,
                        "birth_place": row[5]
                    })
                
                return archived
                
        except Exception as e:
            raise e