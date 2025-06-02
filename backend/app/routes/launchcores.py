from flask import Blueprint, jsonify, request
from app.controllers.launchcores_controller import LaunchCoresController

launchcores_bp = Blueprint("launchcores", __name__)

launchcores_controller = LaunchCoresController()


@launchcores_bp.route("/", methods=["GET"])
def get_launchcores():
    try:
        launchcores = launchcores_controller.get_all_launchcores()

        if not launchcores:
            return jsonify({"error": "There is no launchcores!"})

        return jsonify(launchcores), 200

    except Exception as e:
        return jsonify({"error": "Error Getting launchcores", "details": str(e)}), 500
