class User:
    def __init__(self, id, username, email, senha, foto_perfil=None):
        self.id = id
        self.username = username
        self.email = email
        self.senha = senha
        self.foto_perfil = foto_perfil
    
    def to_dict(self, include_senha=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "foto_perfil": self.foto_perfil
        }
        
        if include_senha:
            data["senha"] = self.senha
        
        return data
    
    def to_public_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "foto_perfil": self.foto_perfil
        }
    
    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' email='{self.email}'>"

    def __str__(self):
        return self.username
