import bcrypt
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from Repositories.userRepository import UserRepository
from Utils.valid_email import is_valid_email
from Utils.valid_username import is_valid_username, get_username_error

load_dotenv()

repo = UserRepository()
SECRET_KEY = os.getenv('SECRET_KEY')

class UserWorker:
    def register(self, username, email, senha):
        if not is_valid_email(email):
            return {"error": "E-Mail inválido"}, 400
        if not is_valid_username(username):
            return {"error": get_username_error(username)}, 400
        
        if repo.find_by_username(username):
            return {"error": "Username já existente"}, 401
        if repo.find_by_email(email):
            return {"error": "E-Mail já existente"}, 401
        
        hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        user = repo.create(username, email, hashed.decode("utf-8"))
        
        if not user:
            return {"error": "Erro ao criar usuário"}, 500
        return {"message": "Usuário criado com sucesso!"}
    
    def login(self, email, senha):
        user = repo.find_by_email(email)
        if not user or not bcrypt.checkpw(senha.encode("utf-8"), user.senha.encode("utf-8")):
            return {"error": "Credenciais inválidas"}, 401
        
        access_token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(hours=1),
                "type": "access"
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        refresh_token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(days=7),
                "type": "refresh"
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }

    def get_public_profile(self, username):
        user = repo.get_public_profile(username)
        if user is None:
            return {"error": "Usuário não encontrado"}, 404
        return user

    def update_foto_perfil(self, usuario_id, image_url):
        sucesso = repo.update_foto(usuario_id, image_url)
        if not sucesso:
            return {"error": "Erro ao alterar foto de perfil"}, 500
        return {
            "message": "Foto de perfil atualizada com sucesso",
            "foto_perfil": image_url
        }

    def update_username(self, usuario_id, new_username, password):
        user = repo.find_by_id(usuario_id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404

        if not bcrypt.checkpw(password.encode("utf-8"), user.senha.encode("utf-8")):
            return {"error": "Senha incorreta"}, 401

        if len(new_username) < 3 or len(new_username) > 20:
            return {"error": "Username deve ter entre 3 e 20 caracteres"}, 400

        existing_user = repo.find_by_username(new_username)
        if existing_user and existing_user.id != usuario_id:
            return {"error": "Username já está em uso"}, 400

        sucesso = repo.update_username(usuario_id, new_username)
        if not sucesso:
            return {"error": "Erro ao atualizar username"}, 500
        return {
            "message": "Username atualizado com sucesso",
            "username": new_username
        }

    def update_email(self, usuario_id, new_email, password):
        user = repo.find_by_id(usuario_id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404

        if not bcrypt.checkpw(password.encode("utf-8"), user.senha.encode("utf-8")):
            return {"error": "Senha incorreta"}, 401

        existing_user = repo.find_by_email(new_email)
        if existing_user and existing_user.id != usuario_id:
            return {"error": "E-mail já está em uso"}, 400

        sucesso = repo.update_email(usuario_id, new_email)
        if not sucesso:
            return {"error": "Erro ao atualizar e-mail"}, 500
        return {
            "message": "E-mail atualizado com sucesso",
            "email": new_email
        }

    def update_password(self, usuario_id, current_password, new_password):
        user = repo.find_by_id(usuario_id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404

        if not bcrypt.checkpw(current_password.encode("utf-8"), user.senha.encode("utf-8")):
            return {"error": "Senha atual incorreta"}, 401

        if len(new_password) < 6:
            return {"error": "Nova senha deve ter no mínimo 6 caracteres"}, 400

        new_password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        sucesso = repo.update_password(usuario_id, new_password_hash.decode("utf-8"))
        
        if not sucesso:
            return {"error": "Erro ao atualizar senha"}, 500
        return {"message": "Senha atualizada com sucesso"}

    def delete_account(self, usuario_id, password):
        user = repo.find_by_id(usuario_id)
        if not user:
            return {"error": "Usuário não encontrado"}, 404

        if not bcrypt.checkpw(password.encode("utf-8"), user.senha.encode("utf-8")):
            return {"error": "Senha incorreta"}, 401

        sucesso = repo.delete_user(usuario_id)
        if not sucesso:
            return {"error": "Erro ao excluir conta"}, 500
        return {"message": "Conta excluída com sucesso"}
