from Utils.db_railway import get_db
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

    def get_public_profile(self, username):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, foto_perfil FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return None

        cursor.execute("SELECT id, titulo, url, ordem FROM links WHERE usuario_id = %s ORDER BY ordem ASC", (user["id"],))
        links = cursor.fetchall()

        cursor.close()
        conn.close()

        user["links"] = links
        return user

    def update_foto(self, usuario_id, image_url):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET foto_perfil = %s WHERE id = %s",
            (usuario_id, image_url)
        )
        conn.commit()
        cursor.close()
        conn.close()