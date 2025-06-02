from flask import Blueprint
from app.routes.example import example_bp
from app.routes.rockets import rockets_bp
from app.routes.cores import cores_bp
from app.routes.orbital import orbitals_bp
from app.routes.crews import crews_bp
from app.routes.launchpads import launchpads_bp
from app.routes.launches import launches_bp
from app.routes.launchcores import launchcores_bp
from app.routes.payloads import payloads_bp
from app.routes.starlinksatellites import starlinksatellites_bp


api_bp = Blueprint("api", __name__, url_prefix="/api")

# Register the example blueprint with the api blueprint
api_bp.register_blueprint(example_bp, url_prefix="/example")
api_bp.register_blueprint(rockets_bp, url_prefix="/rockets")
api_bp.register_blueprint(cores_bp, url_prefix="/cores")
api_bp.register_blueprint(orbitals_bp, url_prefix="/orbitals")
api_bp.register_blueprint(crews_bp, url_prefix="/crews")
api_bp.register_blueprint(launchpads_bp, url_prefix="/launchpads")
api_bp.register_blueprint(launches_bp, url_prefix="/launches")
api_bp.register_blueprint(launchcores_bp, url_prefix="/launchcores")
api_bp.register_blueprint(payloads_bp, url_prefix="/payloads")
api_bp.register_blueprint(starlinksatellites_bp, url_prefix="/starlinksatellites")
