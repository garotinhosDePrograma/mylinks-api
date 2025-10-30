from flask import Blueprint, request, jsonify, redirect
from flask_cors import cross_origin
import cloudinary
import cloudinary.uploader
import jwt
from datetime import datetime, timedelta
from Workers.userWorker import UserWorker
from Utils.auth import token_required
import os
from dotenv import load_dotenv

load_dotenv()

user_bp = Blueprint("usuario", __name__)
worker = UserWorker()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@user_bp.route("/auth/register", methods=["POST"])
@cross_origin()
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    senha = data.get("senha")
    if not all([username, email, senha]):
        return jsonify({"error": "Campos Obrigatórios"}), 400
    return worker.register(username, email, senha)

@user_bp.route("/auth/login", methods=["POST"])
@cross_origin()
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    return worker.login(email, senha)

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

        return jsonify({"access_token": new_access_token})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

@user_bp.route("/user/<string:username>", methods=["GET"])
@cross_origin()
def public_profile(username):
    return worker.get_public_profile(username)

@user_bp.route("/<string:username>", methods=["GET"])
def short_url(username):
    return redirect(f"https://mylinks-352x.onrender.com/profile.html?user={username}")

@user_bp.route("/auth/upload", methods=["POST"])
@token_required
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

        return worker.update_foto_perfil(usuario_id, image_url)
    except Exception as e:
        print("Erro no upload:", e)
        return jsonify({"error": "Falha ao enviar imagem"}), 500

@user_bp.route("/auth/update-username", methods=["PUT"])
@token_required
def update_username(usuario_id):
    data = request.get_json()
    new_username = data.get("newUsername")
    password = data.get("password")
    
    if not all([new_username, password]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    return worker.update_username(usuario_id, new_username, password)


@user_bp.route("/auth/update-email", methods=["PUT"])
@token_required
def update_email(usuario_id):
    data = request.get_json()
    new_email = data.get("newEmail")
    password = data.get("password")
    
    if not all([new_email, password]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    return worker.update_email(usuario_id, new_email, password)


@user_bp.route("/auth/update-password", methods=["PUT"])
@token_required
def update_password(usuario_id):
    data = request.get_json()
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")
    
    if not all([current_password, new_password]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    return worker.update_password(usuario_id, current_password, new_password)


@user_bp.route("/auth/delete-account", methods=["DELETE"])
@token_required
def delete_account(usuario_id):
    data = request.get_json()
    password = data.get("password")
    
    if not password:
        return jsonify({"error": "Senha é obrigatória"}), 400
    return worker.delete_account(usuario_id, password)