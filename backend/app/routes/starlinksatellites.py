from flask import Blueprint, jsonify, request
from app.controllers.starlinksatellites_controller import StarlinkSatellitesController

starlinksatellites_bp = Blueprint("starlink_satellites", __name__)

starlinksatellites_controller = StarlinkSatellitesController()


@starlinksatellites_bp.route("/", methods=["GET"])
def get_starlinksatellites():
    try:
        starlinksatellites = starlinksatellites_controller.get_all_starlinksatellites()

        if not starlinksatellites:
            return jsonify({"error": "There is no starlinksatellites!"})

        return jsonify(starlinksatellites), 200

    except Exception as e:
        return jsonify({"error": "Error Getting starlinksatellites", "details": str(e)}), 500

@starlinksatellites_bp.route("/columns", methods=["GET"])
def get_columns():
    try:
        keys = starlinksatellites_controller.get_columns()

        if not keys:
            return jsonify({"error": "There is no starlinksatellites!"})

        return jsonify(keys), 200

    except Exception as e:
        return jsonify({"error": "Error getting columns", "details": str(e)}), 500
