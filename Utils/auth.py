from flask import request, jsonify
import jwt
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            bearer = request.headers["Authorization"]
            token = bearer.replace("Bearer ", "")

        if not token:
            return jsonify({"error": "Token não fornecido"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["id"]
        except Exception as e:
            return jsonify({"error": "Token inválido ou expirado"}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated