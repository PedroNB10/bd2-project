from flask import Blueprint, jsonify, request
from app.controllers.payloads_controller import PayloadsController

payloads_bp = Blueprint("payloads", __name__)

payloads_controller = PayloadsController()


@payloads_bp.route("/", methods=["GET"])
def get_payloads():
    try:
        payloads = payloads_controller.get_all_payloads()

        if not payloads:
            return jsonify({"error": "There is no payloads!"})

        return jsonify(payloads), 200

    except Exception as e:
        return jsonify({"error": "Error Getting payloads", "details": str(e)}), 500

@payloads_bp.route("/columns", methods=["GET"])
def get_columns():
    try:
        keys = payloads_controller.get_columns()

        if not keys:
            return jsonify({"error": "There is no payloads!"})

        return jsonify(keys), 200

    except Exception as e:
        return jsonify({"error": "Error getting columns", "details": str(e)}), 500
