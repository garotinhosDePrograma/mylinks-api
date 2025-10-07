from Utils.db import get_db
from Models.user import User

class UserRepository:
    def create(self, username, email, senha):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (username, email, senha) VALUES (%s, %s, %s)",
            (username, email, senha)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True