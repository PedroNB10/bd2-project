from flask import Blueprint, jsonify, request
from app.controllers.example_controller import ExampleController

example_bp = Blueprint("example", __name__)


@example_bp.route("/", methods=["GET"])
def get_example():
    """
    Example GET endpoint that returns a simple message with current timestamp
    """
    response_data, status_code = ExampleController.get_example()
    return jsonify(response_data), status_code


@example_bp.route("/", methods=["POST"])
def create_example():
    """
    Example POST endpoint that accepts JSON data and returns it with a timestamp
    """
    data = request.get_json()
    response_data, status_code = ExampleController.create_example(data)
    return jsonify(response_data), status_code
