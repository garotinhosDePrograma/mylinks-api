from Utils.db_railway import get_db
from mysql.connector import Error
from Models.link import Link
import logging

logging.basicConfig(level=logging.ERROR)

class LinkRepository:
    def getAll(self, usuario_id):
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, usuario_id, titulo, url, ordem FROM links WHERE usuario_id = %s ORDER BY ordem ASC",
                (usuario_id,)
            )
            links = cursor.fetchall()
            cursor.close()
            conn.close()

            if links:
                return [Link(**links) for link in links]
            return []
        
        except Error as e:
            logging.error(f"Erro ao tentar buscar links: {e}")
            return None

    def create(self, usuario_id, titulo, url, ordem):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO links (usuario_id, titulo, url, ordem) VALUES (%s, %s, %s, %s)",
                (usuario_id, titulo, url, ordem)
            )
            link_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()

            return Link(
                id=link_id,
                usuario_id=usuario_id,
                titulo=titulo,
                url=url,
                ordem=ordem
            )
        
        except Error as e:
            logging.error(f"Erro ao tentar criar link: {e}")
            return False

    def find_by_id(self, link_id, usuario_id):
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM links WHERE id = %s AND usuario_id = %s",
                (link_id, usuario_id)
            )
            link = cursor.fetchone()
            cursor.close()
            conn.close()

            if link:
                return Link(**link)
            return []
        
        except Error as e:
            logging.error(f"Erro ao tentar buscar link por ID: {e}")
            return None

    def update(self, titulo, url, id, usuario_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE links SET titulo = %s, url = %s WHERE id = %s AND usuario_id = %s",
                (titulo, url, id, usuario_id)
            )
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            return rows_affected > 0
            
        except Error as e:
            logging.error(f"Erro ao tentar atualizar link: {e}")
            return False
    
    def delete(self, id, usuario_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM links WHERE id = %s AND usuario_id = %s",
                (id, usuario_id)
            )
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            return rows_affected > 0
            
        except Error as e:
            logging.error(f"Erro ao tentar deletar link: {e}")
            return False

    def reorder(self, usuario_id, links):
        try:
            conn = get_db()
            cursor = conn.cursor()
            for link in links:
                cursor.execute(
                    "UPDATE links SET ordem = %s WHERE id = %s AND usuario_id = %s",
                    (link["ordem"], link["id"], usuario_id)
                )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            logging.error(f"Erro ao tentar reordenar links: {e}")
            return False

    def count_by_user(self, usuario_id):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM links WHERE usuario_id = %s",
                (usuario_id,)
            )
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            return count
        
        except Error as e:
            logging.error(f"Erro ao contar links: {e}")
            return 0
