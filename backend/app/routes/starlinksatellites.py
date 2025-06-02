from flask import Blueprint, jsonify, request
from app.controllers.starlinksatellites_controller import StarlinkSatellitesController

starlinksatellites_bp = Blueprint("starlinksatellites", __name__)

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
