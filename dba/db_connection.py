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


def get_connection(database=DB_NAME, user=DB_USER, password=DB_PASS):
    db_config = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": user,
        "password": password,
        "dbname": database
    }

    print("Current User:", db_config)
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=database, user=user, password=password
    )