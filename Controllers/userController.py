from flask import Blueprint, request, jsonify
import cloudinary
import cloudinary.uploader
from Workers.userWorker import UserWorker
from werkzeug.utils import secure_filename
from Utils.auth import token_required
import os

user_bp = Blueprint("usuario", __name__)
worker = UserWorker()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@user_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    senha = data.get("senha")
    if not all([username, email, senha]):
        return jsonify({"error": "Campos Obrigatórios"}), 400
    return jsonify(worker.register(username, email, senha))

@user_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    return jsonify(worker.login(email, senha))

@user_bp.route("/user/<string:username>", methods=["GET"])
def public_profile(username):
    return jsonify(worker.get_public_profile(username))

@user_bp.route("/auth/upload", methods=["POST"])
@token_required
def upload_foto(usuario_id):
    print(request.files)
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
        return jsonify(worker.update_foto_perfol(usuario_id, image_url))
    
    except Exception as e:
        print("Erro no upload:", e)
        return jsonify({"error": "Falha ao enviar imagem"}), 500
