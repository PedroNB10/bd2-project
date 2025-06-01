from flask import Blueprint, jsonify, request
from app.controllers.launches_controller import LaunchesController

launches_bp = Blueprint("launches", __name__)

launches_controller = LaunchesController()


@launches_bp.route("/", methods=["GET"])
def get_launches():
    try:
        launches = launches_controller.get_all_launches()

        if not launches:
            return jsonify({"error": "There is no launches!"})

        return jsonify(launches), 200

    except Exception as e:
        return jsonify({"error": "Error Getting launches", "details": str(e)}), 500
