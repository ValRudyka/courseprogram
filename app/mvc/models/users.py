import bcrypt
from sqlalchemy import create_engine

class UserModel:
    def __init__(self, engine):
        self.engine = engine
        
    def create_user(self, username: str, password: str) -> str | None:        
        try:
            with self.engine.connect() as cursor:
                result = cursor.execute(""" 
                    SELECT username FROM Users WHERE username = :username;
                """, {"username": username})

                if result.fetchone():
                    raise "Такий користувач вже існує, спробуйте увійти з таким логіном!"
                
                password_hash = self._hash_password(password)
                max_id = cursor.execute("SELECT MAX(user_id) FROM Users")
                id = 1 if max_id.scalar() is None else max_id.scalar() + 1

                cursor.execute(
                    f"""
                     INSERT INTO Users VALUES ({id}, {username}, {password_hash})
                    """)
                
        except Exception as e:
            return e
        
    def authenticate(self, username: str, password: str) -> str | dict:
        try:
            with self.engine.connect() as cursor:
                result = cursor.execute(""" 
                    SELECT * FROM Users WHERE username = :username;
                """, {"username": username})

                row = result.fetchone()

                if not row:
                    raise "Користувач відсутній в системі. Спробуйте зареєструватися!"
                
                user_id, username, password_hash = row

                if not self._verify_password(password, password_hash):
                    raise "Пароль введений неправильно. Спробуйте ще раз!"

                user = {'user_id': user_id, 'username': username}

                return user
        except Exception as e:
            return e
        
    def _hash_password(self, password: str) -> str:
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)

        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(password, stored_hash)


