from Utils.db_railway import get_db

class LinkRepository:
    def getAll(self, usuario_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM links WHERE usuario_id = %s ORDER BY ordem ASC", (usuario_id,))
        links = cursor.fetchall()
        cursor.close()
        conn.close()
        return links

    def create(self, usuario_id, titulo, url, ordem):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO links (usuario_id, titulo, url, ordem) VALUES (%s, %s, %s, %s)",
            (usuario_id, titulo, url, ordem)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def update(self, titulo, url, id, usuario_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE links SET titulo = %s, url = %s WHERE id = %s AND usuario_id = %s", (titulo, url, id, usuario_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    def delete(self, id, usuario_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM links WHERE id = %s AND usuario_id = %s", (id, usuario_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def reorder(self, usuario_id, links):
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
