import psycopg2
import psycopg
import time
import os
import sys

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from backend.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASS,
    DB_NAME,
)


def get_connection(database=DB_NAME):
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=database, user=DB_USER, password=DB_PASS
    )


def wait_for_db(retry_delay=2, max_retries=60):
    """
    Wait until the database is ready before starting the application.
    """
    db_config = {
        "host": DB_HOST or "localhost",
        "port": DB_PORT or "5432",
        "user": DB_USER or "postgres",
        "password": DB_PASS or "root",
        "dbname": DB_NAME or "spacex_bd2",
    }

    print("Using database configuration:", db_config)
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg.connect(**db_config)
            conn.close()
            print("Database is available!")
            return
        except psycopg.OperationalError:
            print(f"Database not available yet, waiting {retry_delay} seconds...")
            time.sleep(retry_delay)
            retries += 1

    raise RuntimeError("Database did not become available after several retries.")
