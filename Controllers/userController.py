from flask import Blueprint, request, jsonify, redirect
from flask_cors import cross_origin
import cloudinary
import cloudinary.uploader
import jwt
from datetime import datetime, timedelta
from Workers.userWorker import UserWorker
from werkzeug.utils import secure_filename
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

# ==============================================
# 🔐 REGISTRO E LOGIN
# ==============================================
@user_bp.route("/auth/register", methods=["POST"])
@cross_origin()
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    senha = data.get("senha")
    if not all([username, email, senha]):
        return jsonify({"error": "Campos Obrigatórios"}), 400
    return jsonify(worker.register(username, email, senha))

@user_bp.route("/auth/login", methods=["POST"])
@cross_origin()
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    return jsonify(worker.login(email, senha))

# ==============================================
# ♻️ REFRESH TOKEN
# ==============================================
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

        # ✅ Corrigido: usar o id do token decodificado
        new_access_token = jwt.encode(
            {"id": decoded["id"], "exp": datetime.utcnow() + timedelta(hours=1)},
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        return jsonify({"access_token": new_access_token})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

# ==============================================
# 👤 PERFIL PÚBLICO
# ==============================================
@user_bp.route("/user/<string:username>", methods=["GET"])
@cross_origin()
def public_profile(username):
    return jsonify(worker.get_public_profile(username))

# ==============================================
# 🔗 REDIRECIONAMENTO DE PERFIL
# ==============================================
@user_bp.route("/<string:username>", methods=["GET"])
def short_url(username):
    return redirect(f"https://mylinks-352x.onrender.com/profile.html?user={username}")

# ==============================================
# 🖼️ UPLOAD DE FOTO DE PERFIL
# ==============================================
@user_bp.route("/auth/upload", methods=["POST"])
@token_required
@cross_origin()
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

        return jsonify(worker.update_foto_perfil(usuario_id, image_url))
    except Exception as e:
        print("Erro no upload:", e)
        return jsonify({"error": "Falha ao enviar imagem"}), 500
