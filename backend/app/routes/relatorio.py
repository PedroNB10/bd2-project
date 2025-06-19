from flask import Blueprint, request, jsonify
from app.controllers.relatorio import RelatorioController

relatorio_bp = Blueprint("relatorio", __name__)

relatorio = RelatorioController()

@relatorio_bp.route("/", methods=["POST"])
def rota_relatorio_dados():
    payload = request.get_json()
    return relatorio.relatorio_dados(payload)