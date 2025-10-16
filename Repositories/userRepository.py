from Utils.db_railway import get_db
from Models.user import User
from mysql.connector import Error

class UserRepository:
    def create(self, username, email, senha):
        try:
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
        except Error as e:
            print(f"ERRO: {e}")

    def find_by_email(self, email):
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Error as e:
            print(f"ERRO: {e}")
    
    def find_by_username(self, username):
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Error as e:
            print(f"ERRO: {e}")

    def get_public_profile(self, username):
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, foto_perfil FROM usuarios WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user or user == null or user is None:
                cursor.close()
                conn.close()
                return None

            cursor.execute("SELECT id, titulo, url, ordem FROM links WHERE usuario_id = %s ORDER BY ordem ASC", (user["id"],))
            links = cursor.fetchall()

            cursor.close()
            conn.close()

            user["links"] = links
            return user
        except Error as e:
            print(f"ERRO: {e}")

    def update_foto(self, usuario_id, image_url):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET foto_perfil = %s WHERE id = %s",
                (image_url, usuario_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"ERRO: {e}")
