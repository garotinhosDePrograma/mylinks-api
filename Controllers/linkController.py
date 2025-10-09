from flask import Blueprint, request, jsonify
from Worker.linkWorker import LinkWorker
from Utils.auth import token_required

link_bp = Blueprint("links", __name__)
worker = LinkWorker()

@link_bp.route("/links", methods=["GET"])
@token_required
def listar_links(usuario_id):
    return jsonify(worker.listar(usuario_id))

@link_bp.route("/links", methods=["POST"])
@token_required
def criar_link(usuario_id):
    data = request.get_json()
    titulo = data.get("titulo")
    url = data.get("url")
    if not all([titulo, url]):
        return jsonify({"error": "Campos Obrigatórios"}), 400
    return jsonify(worker.create(usuario_id, titulo, url))
