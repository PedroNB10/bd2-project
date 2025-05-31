from flask import Blueprint
from app.routes.example import example_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.register_blueprint(example_bp, url_prefix="/example")
