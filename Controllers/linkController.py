from flask import Blueprint, request, jsonify
from Workers.linkWorker import LinkWorker
from Utils.auth import token_required

link_bp = Blueprint("links", __name__)
worker = LinkWorker()

@link_bp.route("/links", methods=["GET"])
@token_required
def get_links(usuario_id):
    return jsonify(worker.getAll(usuario_id))

@link_bp.route("/links", methods=["POST"])
@token_required
def create_link(usuario_id):
    data = request.get_json()
    titulo = data.get("titulo")
    url = data.get("url")
    if not all([titulo, url]):
        return jsonify({"error": "Campos Obrigatórios"}), 400
    return jsonify(worker.create(usuario_id, titulo, url))

@link_bp.route("/links/<int:id>", methods=["PUT"])
@token_required
def update_link(usuario_id, id):
    data = request.get_json()
    titulo = data.get("titulo")
    url = data.get("url")
    return jsonify(worker.update(titulo, url, id, usuario_id))

@link_bp.route("/links/<int:id>", methods=["DELETE"])
@token_required
def delete_link(usuario_id, id):
    return jsonify(worker.delete(usuario_id, id))

@link_bp.route("/links/reorder", methods=["PUT"])
@token_required
def reorder_links(usuario_id):
    data = request.get_json()
    return jsonify(worker.reorder(usuario_id, data))



