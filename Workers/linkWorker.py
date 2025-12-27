from Repositories.linkRepository import LinkRepository
from Utils.valid_url import is_valid_url, get_url_error

repo = LinkRepository()

class LinkWorker:
    def getAll(self, usuario_id):
        links = repo.getAll(usuario_id)
        if links is None:
            return {"error": "Erro ao buscar links"}, 500
        
        return [link.to_dict() for link in links]
    
    def create(self, usuario_id, titulo, url):
        links = repo.getAll(usuario_id)
        if links is None:
            return {"error": "Erro ao buscar links existentes"}, 500
        
        url_valida = is_valid_url(url)
        if not url_valida:
            return {"error": get_url_error(url)}, 400

        nova_ordem = len(links) + 1
        link = repo.create(usuario_id, titulo, url, nova_ordem)
        
        if not link:
            return {"error": "Erro ao adicionar link"}, 500
        return {"message": "Link adicionado com sucesso"}
    
    def update(self, titulo, url, id, usuario_id):
        url_valida = is_valid_url(url)
        if not url_valida:
            return {"error": get_url_error(url)}, 400
        
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
        if not links or not isinstance(links, list):
            return {"error": "Lista de links inválida"}, 400

        for link in links:
            if not isinstance(link, dict) or "id" not in link or "ordem" not in link:
                return {"error": "Formato de link inválido"}, 400
        
        sucesso = repo.reorder(usuario_id, links)
        
        if not sucesso:
            return {"error": "Erro ao reordenar links"}, 500
        return {"message": "Links reordenados com sucesso"}

    def get_by_id(self, link_id, usuario_id):
        link = repo.find_by_id(link_id, usuario_id)
        if not link:
            return {"error": "Link não encontrado"}, 400
        return link.to_dict()
