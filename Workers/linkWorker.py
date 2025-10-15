from Repositories.linkRepository import LinkRepository

repo = LinkRepository()

class LinkWorker:
    def getAll(self, usuario_id):
        return repo.getAll(usuario_id)
    
    def create(self, usuario_id, titulo, url):
        links = repo.getAll(usuario_id)
        nova_ordem = len(links) + 1
        repo.create(usuario_id, titulo, url, nova_ordem)
        return {"message": "Link adicionado com sucesso"}
    
    def update(self, usuario_id, id, titulo, url):
        repo.update(id, usuario_id, titulo, url)
        return {"message": "Link atualizado com sucesso"}
    
    def delete(self, usuario_id, id):
        repo.delete(id, usuario_id)
        return {"message": "Link removido com sucesso"}

    def reorder(self, usuario_id, links):
        repo.reorder(usuario_id, links)
        return {"message": "Links reordenados com sucesso"}
