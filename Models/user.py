class User:
    def __init__(self, id, username, email, senha, foto_perfil=None):
        self.id = id
        self.username = username
        self.email = email
        self.senha = senha
        self.foto_perfil = foto_perfil