from flask import Blueprint
from app.routes.example import example_bp
from app.routes.rockets import rockets_bp


api_bp = Blueprint("api", __name__, url_prefix="/api")

# Register the example blueprint with the api blueprint
api_bp.register_blueprint(example_bp, url_prefix="/example")
api_bp.register_blueprint(rockets_bp, url_prefix="/rockets")
