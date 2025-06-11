from flask import Blueprint, jsonify, request
from app.controllers.orbital_controller import OrbitalsController

orbitals_bp = Blueprint("orbitals", __name__)

orbitals_controller = OrbitalsController()


@orbitals_bp.route("/", methods=["GET"])
def get_orbitals():
    try:
        orbitals = orbitals_controller.get_all_orbitals()

        if not orbitals:
            return jsonify({"error": "There is no orbitals!"})

        return jsonify(orbitals), 200

    except Exception as e:
        return jsonify({"error": "Error Getting Orbitals", "details": str(e)}), 500

@orbitals_bp.route("/columns", methods=["GET"])
def get_columns():
    try:
        keys = orbitals_controller.get_columns()

        if not keys:
            return jsonify({"error": "There is no orbitals!"})

        return jsonify(keys), 200

    except Exception as e:
        return jsonify({"error": "Error getting columns", "details": str(e)}), 500
