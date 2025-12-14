from flask import Blueprint, request, jsonify, redirect
from flask_cors import cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import cloudinary
import cloudinary.uploader
import jwt
from datetime import datetime, timedelta
from Workers.userWorker import UserWorker
from Utils.auth import token_required
from Utils.cloudinary import configure_cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

user_bp = Blueprint("usuario", __name__)
worker = UserWorker()

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limites=["200 per day", "50 per hour"]
)

configure_cloudinary()

@user_bp.route("/auth/register", methods=["POST"])
@cross_origin()
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    username = data.get("username")
    email = data.get("email")
    senha = data.get("senha")
    
    if not all([username, email, senha]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    result = worker.register(username, email, senha)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_bp.route("/auth/login", methods=["POST"])
@cross_origin()
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    email = data.get("email")
    senha = data.get("senha")
    
    if not all([email, senha]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    result = worker.login(email, senha)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_bp.route("/auth/refresh", methods=["POST"])
@cross_origin()
def refresh_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token não fornecido"}), 401

    token = auth_header.split(" ")[1] if " " in auth_header else auth_header

    try:
        decoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

        if decoded.get("type") != "refresh":
            return jsonify({"error": "Token inválido para refresh"}), 401

        new_access_token = jwt.encode(
            {"id": decoded["id"], "exp": datetime.utcnow() + timedelta(hours=1), "type": "access"},
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        return jsonify({"access_token": new_access_token}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

@user_bp.route("/user/<string:username>", methods=["GET"])
@cross_origin()
def public_profile(username):
    result = worker.get_public_profile(username)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_bp.route("/<string:username>", methods=["GET"])
def short_url(username):
    return redirect(f"https://mylinks-352x.onrender.com/profile.html?user={username}")

@user_bp.route("/auth/upload", methods=["POST"])
@token_required
@limiter.limit("5 per minute")
def upload_foto(usuario_id):
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Arquivo inválido"}), 400

    extensoes = {"png", "jpg", "jpeg"}
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in extensoes:
        return jsonify({"error": "Formato não permitido"}), 400

    try:
        upload_result = cloudinary.uploader.upload(
            file,
            folder="mylinks_profiles",
            public_id=f"user_{usuario_id}",
            overwrite=True,
            resource_type="image"
        )

        image_url = upload_result["secure_url"]
        result = worker.update_foto_perfil(usuario_id, image_url)
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result), 200
        
    except Exception as e:
        print("Erro no upload:", e)
        return jsonify({"error": "Falha ao enviar imagem"}), 500

@user_bp.route("/auth/update-username", methods=["PUT"])
@token_required
@limiter.limit("5 per minute")
def update_username(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    new_username = data.get("newUsername")
    password = data.get("password")
    
    if not all([new_username, password]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    result = worker.update_username(usuario_id, new_username, password)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_bp.route("/auth/update-email", methods=["PUT"])
@token_required
@limiter.limit("5 per minute")
def update_email(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    new_email = data.get("newEmail")
    password = data.get("password")
    
    if not all([new_email, password]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    result = worker.update_email(usuario_id, new_email, password)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_bp.route("/auth/update-password", methods=["PUT"])
@token_required
@limiter.limit("5 per minute")
def update_password(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")
    
    if not all([current_password, new_password]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    result = worker.update_password(usuario_id, current_password, new_password)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@user_bp.route("/auth/delete-account", methods=["DELETE"])
@token_required
@limiter.limit("5 per minute")
def delete_account(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    password = data.get("password")
    
    if not password:
        return jsonify({"error": "Senha é obrigatória"}), 400
    
    result = worker.delete_account(usuario_id, password)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200
