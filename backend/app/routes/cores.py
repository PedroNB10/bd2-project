from flask import Blueprint, jsonify, request
from app.controllers.cores_controller import CoresController

cores_bp = Blueprint("cores", __name__)

cores_controller = CoresController()


@cores_bp.route("/", methods=["GET"])
def get_cores():
    try:
        cores = cores_controller.get_all_cores()

        if not cores:
            return jsonify({"error": "There is no cores!"})

        return jsonify(cores), 200

    except Exception as e:
        return jsonify({"error": "Error Getting cores", "details": str(e)}), 500
    
@cores_bp.route("/columns", methods=["GET"])
def get_columns():
    try:
        keys = cores_controller.get_columns()

        if not keys:
            return jsonify({"error": "There is no cores!"})

        return jsonify(keys), 200

    except Exception as e:
        return jsonify({"error": "Error getting columns", "details": str(e)}), 500
