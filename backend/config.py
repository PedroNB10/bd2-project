import os
from dotenv import load_dotenv

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Try to load .env.local first, if it doesn't exist, fall back to .env
env_local_path = os.path.join(project_root, ".env.local")
env_path = os.path.join(project_root, ".env")

if os.path.exists(env_local_path):
    print('envLocal')
    load_dotenv(env_local_path)
else:
    print('env')
    load_dotenv(env_path)

# Define configuration variables with defaults if not provided
USE_DOCKER = os.getenv("USE_DOCKER", "true").lower() == "true"

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "root")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "4000" if USE_DOCKER else "5432")
DB_NAME = os.getenv("POSTGRES_DB", "spacex_bd2")
DB_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")

# Construct the database URI
SQL_DATABASE_URI = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)