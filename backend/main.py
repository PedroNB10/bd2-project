import subprocess
from app import create_app, wait_for_db
from config import USE_DOCKER

if __name__ == "__main__":
    try:
        print(f"USE_DOCKER: ", USE_DOCKER)
        if USE_DOCKER:
            print("Starting Docker Compose...")
            subprocess.run(["docker", "compose", "up", "-d"], check=True)

        wait_for_db()

        app = create_app()
        app.run(debug=True, host="0.0.0.0", port=3000)
    except KeyboardInterrupt:
        print("Application interrupted by user.")
    finally:
        if USE_DOCKER:
            print("Stopping Docker Compose...")
            subprocess.run(["docker", "compose", "down"], check=True)
