import bcrypt
from sqlalchemy import text
from datetime import datetime, timedelta

class UserModel:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.login_attempts = {} 
        self.max_attempts = 5    
        self.lockout_duration = 10
        
    def create_user(self, username: str, password: str) -> tuple[bool, str]:        
        try:
            with self.engine.connect() as cursor:
                transaction = cursor.begin()
                result = cursor.execute(text(f'''SELECT username FROM "Users" WHERE username = '{username}';'''))
                
                if result.fetchone():
                    raise Exception("Такий користувач вже існує, спробуйте увійти з таким логіном!")
                
                password_hash = self._hash_password(password)
                cursor.execute(text(f"INSERT INTO \"Users\" (username, password_hash, last_login, failed_attempts) VALUES (:username, :password_hash, NULL, 0)"), 
                              {"username": username, "password_hash": password_hash})

                transaction.commit()
                return True, "Успішно додано користувача, переходимо до головної форми!"
                
        except BaseException as e:
            print(e)
            return False, str(e)
        
    def authenticate(self, username: str, password: str) -> tuple[bool, dict|str]:
        try:
            if username in self.login_attempts:
                attempts_info = self.login_attempts[username]
                if attempts_info["count"] >= self.max_attempts:
                    time_diff = datetime.now() - attempts_info["timestamp"]
                    if time_diff.total_seconds() < self.lockout_duration * 60:
                        remaining_minutes = self.lockout_duration - int(time_diff.total_seconds() / 60)
                        raise Exception(f"Обліковий запис тимчасово заблоковано. Спробуйте через {remaining_minutes} хвилин.")
                    else:
                        self.login_attempts[username]["count"] = 0
            
            with self.engine.connect() as cursor:
                transaction = cursor.begin()
                result = cursor.execute(text("""SELECT * FROM "Users" WHERE username = :username;"""), {"username": username})
                row = result.fetchone()

                if not row:
                    self._increment_failed_attempt(username)
                    raise Exception("Користувач відсутній в системі. Спробуйте зареєструватися!")

                user_id, username, password_hash = row[:3]

                if not self._verify_password(password, password_hash):
                    self._increment_failed_attempt(username)
                    attempts_left = self.max_attempts - self.login_attempts[username]["count"]
                    raise Exception(f"Пароль введений неправильно. Залишилось спроб: {attempts_left}")

                if username in self.login_attempts:
                    del self.login_attempts[username]
                
                cursor.execute(text("""
                    UPDATE "Users" 
                    SET last_login = CURRENT_TIMESTAMP, failed_attempts = 0 
                    WHERE username = :username
                """), {"username": username})
                
                transaction.commit()

                user = {'user_id': user_id, 'username': username}
                return True, user
                
        except BaseException as e:
            print(e)
            return False, str(e)
    
    def _increment_failed_attempt(self, username):
        """Increment the failed login attempts counter for a username"""
        if username not in self.login_attempts:
            self.login_attempts[username] = {"count": 0, "timestamp": datetime.now()}
        
        self.login_attempts[username]["count"] += 1
        self.login_attempts[username]["timestamp"] = datetime.now()
        
        try:
            with self.engine.connect() as cursor:
                transaction = cursor.begin()
                cursor.execute(text("""
                    UPDATE "Users" 
                    SET failed_attempts = failed_attempts + 1 
                    WHERE username = :username
                """), {"username": username})
                transaction.commit()
        except Exception as e:
            print(f"Error updating failed attempts: {e}")
        
    def _hash_password(self, password: str) -> str:
        password = password.encode('utf-8')
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)

        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        password = password.encode('utf-8')
        stored_hash = stored_hash.encode('utf-8')

        return bcrypt.checkpw(password, stored_hash)
    
    def change_password(self, username: str, new_password: str) -> tuple[bool, str]:
        try:
            password_hash = self._hash_password(new_password)
            
            with self.engine.connect() as conn:
                transaction = conn.begin()
                try:
                    result = conn.execute(
                        text("SELECT COUNT(*) FROM \"Users\" WHERE username = :username"),
                        {"username": username}
                    )
                    user_count = result.scalar()
                    
                    if user_count == 0:
                        transaction.rollback()
                        return False, "Користувача не знайдено"
                    
                    conn.execute(
                        text("""
                        UPDATE "Users" 
                        SET password_hash = :password_hash
                        WHERE username = :username
                        """), 
                        {"username": username, "password_hash": password_hash}
                    )
                    
                    transaction.commit()
                    return True, "Пароль успішно змінено!"
                    
                except Exception as e:
                    transaction.rollback()
                    raise e
                    
        except Exception as e:
            print(f"Error changing password: {e}")
            return False, str(e)