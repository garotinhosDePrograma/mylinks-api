class Link:
    def __init__(self, id, usuario_id, titulo, url, ordem):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.url = url
        self.ordem = ordem
    
    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "titulo": self.titulo,
            "url": self.url,
            "ordem": self.ordem
        }
    
    def __repr__(self):
        return f"<Link id={self.id} titulo='{self.titulo}' ordem={self.ordem}>"
    
    def __str__(self):
        return f"{self.titulo} ({self.url})"
