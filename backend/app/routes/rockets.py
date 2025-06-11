from flask import Blueprint, jsonify, request
from app.controllers.rockets_controller import RocketsController

rockets_bp = Blueprint("rockets", __name__)

rockets_controller = RocketsController()


@rockets_bp.route("/", methods=["GET"])
def get_rockets():
    try:
        rockets = rockets_controller.get_all_rockets()

        if not rockets:
            return jsonify({"error": "There is no rockets!"})

        return jsonify(rockets), 200

    except Exception as e:
        return jsonify({"error": "Error Getting Rockets", "details": str(e)}), 500

@rockets_bp.route("/columns", methods=["GET"])
def get_columns():
    try:
        keys = rockets_controller.get_columns()

        if not keys:
            return jsonify({"error": "There is no rockets!"})

        return jsonify(keys), 200

    except Exception as e:
        return jsonify({"error": "Error getting columns", "details": str(e)}), 500
