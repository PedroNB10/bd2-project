from flask import Blueprint, jsonify, request
from app.controllers.launchpads_controller import LaunchpadsController

launchpads_bp = Blueprint("launchpads", __name__)

launchpads_controller = LaunchpadsController()


@launchpads_bp.route("/", methods=["GET"])
def get_launchpads():
    try:
        launchpads = launchpads_controller.get_all_launchpads()

        if not launchpads:
            return jsonify({"error": "There is no launchpads!"})

        return jsonify(launchpads), 200

    except Exception as e:
        return jsonify({"error": "Error Getting launchpads", "details": str(e)}), 500

@launchpads_bp.route("/columns", methods=["GET"])
def get_columns():
    try:
        keys = launchpads_controller.get_columns()

        if not keys:
            return jsonify({"error": "There is no launchpads!"})

        return jsonify(keys), 200

    except Exception as e:
        return jsonify({"error": "Error getting columns", "details": str(e)}), 500
