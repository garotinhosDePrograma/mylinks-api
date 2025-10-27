from flask import request, jsonify
from functools import wraps
import jwt, os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token de autenticação não fornecido"}), 401

        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header.strip()
        except IndexError:
            return jsonify({"error": "Formato de token inválido"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if decoded.get("type") == "refresh":
                return jsonify({"error": "Use o access token, não o refresh token"}), 401

            user_id = decoded["id"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        except Exception as e:
            print(f"Erro inesperado ao validar token: {e}")
            return jsonify({"error": "Falha ao validar o token"}), 401

        return f(user_id, *args, **kwargs)

    return decorated