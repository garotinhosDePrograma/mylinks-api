from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from Workers.linkWorker import LinkWorker
from Utils.auth import token_required
from Utils.valid_url import is_valid_url

link_bp = Blueprint("links", __name__)
worker = LinkWorker()

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@link_bp.route("/links", methods=["GET"])
@token_required
def get_links(usuario_id):
    result = worker.getAll(usuario_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@link_bp.route("/links", methods=["POST"])
@token_required
@limiter.limit("5 per minute")
def create_link(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    titulo = data.get("titulo")
    url = data.get("url")
    
    if not all([titulo, url]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    if not is_valid_url(url):
        return jsonify({"error": "URL inválida"}), 400
    
    result = worker.create(usuario_id, titulo, url)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@link_bp.route("/links/<int:id>", methods=["PUT"])
@token_required
@limiter.limit("5 per minute")
def update_link(usuario_id, id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    titulo = data.get("titulo")
    url = data.get("url")
    
    if not all([titulo, url]):
        return jsonify({"error": "Campos obrigatórios"}), 400
    
    if not is_valid_url(url):
        return jsonify({"error": "URL inválida"}), 400
    
    result = worker.update(titulo, url, id, usuario_id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@link_bp.route("/links/<int:id>", methods=["DELETE"])
@token_required
@limiter.limit("5 per minute")
def delete_link(usuario_id, id):
    result = worker.delete(usuario_id, id)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result), 200

@link_bp.route("/links/reorder", methods=["PUT"])
@token_required
@limiter.limit("5 per minute")
def reorder_links(usuario_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body inválido"}), 400
    
    result = worker.reorder(usuario_id, data)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 200
