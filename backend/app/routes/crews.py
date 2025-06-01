from flask import Blueprint, jsonify, request
from app.controllers.crews_controller import CrewsController

crews_bp = Blueprint("crews", __name__)

crews_controller = CrewsController()


@crews_bp.route("/", methods=["GET"])
def get_crews():
    try:
        crews = crews_controller.get_all_crews()

        if not crews:
            return jsonify({"error": "There is no crews!"})

        return jsonify(crews), 200

    except Exception as e:
        return jsonify({"error": "Error Getting crews", "details": str(e)}), 500
