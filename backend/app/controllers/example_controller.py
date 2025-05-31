from datetime import datetime
from typing import Dict, Any, Tuple


class ExampleController:
    @staticmethod
    def get_example() -> Tuple[Dict[str, Any], int]:
        """
        Get example data with current timestamp
        Returns:
            Tuple containing response data and status code
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {
                "message": "This is an example endpoint",
                "timestamp": current_time,
                "status": "success",
            }, 200
        except Exception as e:
            return {"error": str(e), "status": "error"}, 500

    @staticmethod
    def create_example(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """
        Process example data and return with timestamp
        Args:
            data: JSON data from request
        Returns:
            Tuple containing response data and status code
        """
        try:
            if not data:
                return {"error": "No data provided", "status": "error"}, 400

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {
                "received_data": data,
                "timestamp": current_time,
                "status": "success",
            }, 201

        except Exception as e:
            return {"error": str(e), "status": "error"}, 500
