from Repositories.linkRepository import LinkRepository

repo = LinkRepository()

class LinkWorker:
    def getAll(self, usuario_id):
        links = repo.getAll(usuario_id)
        if links is None:
            return {"error": "Erro ao buscar links"}, 500
        return links
    
    def create(self, usuario_id, titulo, url):
        links = repo.getAll(usuario_id)
        if links is None:
            return {"error": "Erro ao buscar links existentes"}, 500
        
        nova_ordem = len(links) + 1
        sucesso = repo.create(usuario_id, titulo, url, nova_ordem)
        
        if not sucesso:
            return {"error": "Erro ao adicionar link"}, 500
        return {"message": "Link adicionado com sucesso"}
    
    def update(self, titulo, url, id, usuario_id):
        sucesso = repo.update(titulo, url, id, usuario_id)
        
        if not sucesso:
            return {"error": "Erro ao atualizar link"}, 500
        return {"message": "Link atualizado com sucesso"}
    
    def delete(self, usuario_id, id):
        sucesso = repo.delete(id, usuario_id)
        
        if not sucesso:
            return {"error": "Erro ao remover link"}, 500
        return {"message": "Link removido com sucesso"}

    def reorder(self, usuario_id, links):
        sucesso = repo.reorder(usuario_id, links)
        
        if not sucesso:
            return {"error": "Erro ao reordenar links"}, 500
        return {"message": "Links reordenados com sucesso"}
