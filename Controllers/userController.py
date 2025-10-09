from flask import Blueprint, request, jsonify
from Workers.userWorker import UserWorker

user_bp = Blueprint("usuario", __name__)
worker = UserWorker()

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
def public_profile():
    return jsonify(worker.get_public_profile(username))
