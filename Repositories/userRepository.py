from Utils.db_railway import get_db_cursor
from mysql.connector import Error
from Models.user import User
import logging

logging.basicConfig(level=logging.ERROR)

class UserRepository:
    def create(self, username, email, senha):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (username, email, senha) VALUES (%s, %s, %s)",
                    (username, email, senha)
                )
                user_id = cursor.lastrowid
            
                return User(
                    id=user_id,
                    username=username,
                    email=email,
                    senha=senha
                )
            
        except Error as e:
            logging.error(f"Erro ao tentar criar usuário: {e}")
            return False

    def find_by_email(self, email):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, email, senha, foto_perfil FROM usuarios WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()
            
                if user:
                    return User(**user)
                return None
            
        except Error as e:
            logging.error(f"Erro ao tentar buscar usuário pelo email: {e}")
            return None
    
    def find_by_username(self, username):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, email, senha, foto_perfil FROM usuarios WHERE username = %s",
                    (username,)
                )
                user = cursor.fetchone()
            
                if user:
                    return User(**user)
                return None
            
        except Error as e:
            logging.error(f"Erro ao tentar buscar usuário pelo username: {e}")
            return None

    def find_by_id(self, usuario_id):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, email, senha, foto_perfil FROM usuarios WHERE id = %s",
                    (usuario_id,)
                )
                user = cursor.fetchone()
                
                if user:
                    return User(**user)
                return None
            
        except Error as e:
            logging.error(f"Erro ao tentar buscar usuário pelo ID: {e}")
            return None

    def get_public_profile(self, username):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, foto_perfil FROM usuarios WHERE username = %s",
                    (username,)
                )
                user = cursor.fetchone()

                if not user:
                    return None

                cursor.execute(
                    "SELECT id, titulo, url, ordem FROM links WHERE usuario_id = %s ORDER BY ordem ASC",
                    (user["id"],)
                )
                links = cursor.fetchall()

                return {
                    "id": user["id"],
                    "username": user["username"],
                    "foto_perfil": user["foto_perfil"],
                    "links": links
                }
            
        except Error as e:
            logging.error(f"Erro ao tentar buscar o perfil público: {e}")
            return None

    def update_foto(self, usuario_id, image_url):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET foto_perfil = %s WHERE id = %s",
                    (image_url, usuario_id)
                )
                rows_affected = cursor.rowcount
            
                return rows_affected > 0
            
        except Error as e:
            logging.error(f"Erro ao tentar atualizar a foto de perfil: {e}")
            return False

    def update_username(self, usuario_id, new_username):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET username = %s WHERE id = %s",
                    (new_username, usuario_id)
                )
                rows_affected = cursor.rowcount
            
                return rows_affected > 0
            
        except Error as e:
            logging.error(f"Erro ao tentar atualizar username: {e}")
            return False

    def update_email(self, usuario_id, new_email):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET email = %s WHERE id = %s",
                    (new_email, usuario_id)
                )
                rows_affected = cursor.rowcount
            
                return rows_affected > 0
            
        except Error as e:
            logging.error(f"Erro ao tentar atualizar e-mail: {e}")
            return False

    def update_password(self, usuario_id, new_password_hash):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET senha = %s WHERE id = %s",
                    (new_password_hash, usuario_id)
                )
                rows_affected = cursor.rowcount
            
                return rows_affected > 0
            
        except Error as e:
            logging.error(f"Erro ao tentar atualizar senha: {e}")
            return False

    def delete_user(self, usuario_id):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM usuarios WHERE id = %s",
                    (usuario_id,)
                )
                rows_affected = cursor.rowcount
            
                return rows_affected > 0
        
        except Error as e:
            logging.error(f"Erro ao tentar excluir usuário: {e}")
            return False
