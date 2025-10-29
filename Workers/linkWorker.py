from flask import jsonify
from Repositories.linkRepository import LinkRepository

repo = LinkRepository()

class LinkWorker:
    def getAll(self, usuario_id):
        return repo.getAll(usuario_id)
    
    def create(self, usuario_id, titulo, url):
        links = repo.getAll(usuario_id)
        nova_ordem = len(links) + 1
        sucesso = repo.create(usuario_id, titulo, url, nova_ordem)
        if not sucesso:
            return jsonify({"error": "Erro ao adicionar link"}), 500
        return jsonify({"message": "Link adicionado com sucesso"}), 200
    
    def update(self, titulo, url, id, usuario_id):
        sucesso = repo.update(titulo, url, id, usuario_id)
        if not sucesso:
            return jsonify({"error": "Erro ao adicionar link"}), 500
        return jsonify({"message": "Link atualizado com sucesso"}), 200
    
    def delete(self, usuario_id, id):
        sucesso = repo.delete(id, usuario_id)
        if not sucesso:
            return jsonify({"error": "Erro ao remover link"}), 500
        return jsonify({"message": "Link removido com sucesso"}), 200

    def reorder(self, usuario_id, links):
        sucesso = repo.reorder(usuario_id, links)
        if not sucesso:
            return jsonify({"error": "Erro ao tentar reordenar links"}), 500
        return jsonify({"message": "Links reordenados com sucesso"}), 200