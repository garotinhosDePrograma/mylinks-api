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

    def find_by_email(self, email):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    def find_by_username(self, username):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user