import bcrypt
from sqlalchemy import text

class UserModel:
    def __init__(self, engine) -> None:
        self.engine = engine
        
    def create_user(self, username: str, password: str) -> tuple[bool, str]:        
        try:
            with self.engine.connect() as cursor:
                transaction = cursor.begin()
                result = cursor.execute(text(f'''SELECT username FROM "Users" WHERE username = '{username}';'''))
                
                if result.fetchone():
                    raise Exception("Такий користувач вже існує, спробуйте увійти з таким логіном!")
                
                password_hash = self._hash_password(password)
                cursor.execute(text(f"INSERT INTO \"Users\" (username, password_hash) VALUES (:username, :password_hash)"), {"username": username, "password_hash": password_hash})

                transaction.commit()
                return True, "Успішно додано користувача, переходимо до головної форми!"
                
        except BaseException as e:
            print(e)
            return False, e
        
    def authenticate(self, username: str, password: str) -> tuple[bool, dict|str]:
        try:
            with self.engine.connect() as cursor:
                result = cursor.execute(text("""SELECT * FROM "Users" WHERE username = :username;"""), {"username": username})
                row = result.fetchone()

                if not row:
                    raise Exception("Користувач відсутній в системі. Спробуйте зареєструватися!")
                print(row)
                user_id, username, password_hash = row

                if not self._verify_password(password, password_hash):
                    raise Exception("Пароль введений неправильно. Спробуйте ще раз!")

                user = {'user_id': user_id, 'username': username}

                return True, user
        except BaseException as e:
            print(e)
            return False, e
        
    def _hash_password(self, password: str) -> str:
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)

        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(password, stored_hash)


