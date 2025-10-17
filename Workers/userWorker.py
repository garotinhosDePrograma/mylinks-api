import bcrypt
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from Repositories.userRepository import UserRepository

load_dotenv()

repo = UserRepository()
SECRET_KEY = os.getenv('SECRET_KEY')

class UserWorker:
    def register(self, username, email, senha):
        hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        repo.create(username, email, hashed.decode("utf-8"))
        return {"message": "Usuário criado com sucesso!"}
    
    def login(self, email, senha):
        user = repo.find_by_email(email)
        if not user or not bcrypt.checkpw(senha.encode("utf-8"), user["senha"].encode("utf-8")):
            return {"error": "Credenciais inválidas"}, 401
        
        token = jwt.encode(
            {"id": user["id"], "exp": datetime.utcnow() + timedelta(hours=4)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"token": token, "user": {"id": user["id"], "username": user["username"]}}

    def get_public_profile(self, username):
        user = repo.get_public_profile(username)
        if user is None:
            return {"error": "Usuário não encontrado"}, 404
        return user

    def update_foto_perfil(self, usuario_id, image_url):
        repo.update_foto(usuario_id, image_url)
        return {"message": "Foto de perfil atualizada com sucesso", "foto_perfil": image_url}
