from sqlalchemy import text

class CityModel:
    def __init__(self, engine):
        self.engine = engine
    
    def get_all_cities(self):
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
    
    def get_city_by_id(self, city_id):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                    SELECT c.id_city, c.city_name, co.country_name
                    FROM "Cities" c
                    JOIN "Countries" co ON c.id_country = co.id_country
                    WHERE c.id_city = :id
                    """),
                    {"id": city_id}
                )
                
                row = result.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "name": row[1],
                        "country": row[2],
                        "display_name": f"{row[1]}, {row[2]}"
                    }
                return None
                
        except Exception as e:
            raise e