from db_connection import get_connection, wait_for_db
import subprocess
from backend.config import USE_DOCKER
import psycopg2
from backend.config import DB_NAME

from create_indexes import create_indexes
from users_and_privileges import create_users, define_privileges
from create_tables import create_tables

def drop_user_if_exists(cur, username):
    # Verifica se o usuário existe
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (username,))
    if cur.fetchone():
        cur.execute(f"DROP OWNED BY {username} CASCADE;")
        cur.execute(f"DROP ROLE {username};")

def create_database():
    conn = None
    cur = None
    try:
        conn = get_connection("postgres")
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{DB_NAME}';
            """
        )

        cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cur.execute(f"CREATE DATABASE {DB_NAME}")

        drop_user_if_exists(cur, "spacex_dba")
        drop_user_if_exists(cur, "spacex_api")
        drop_user_if_exists(cur, "spacex_app")

        print(f"Banco {DB_NAME} recriado e usuários antigos excluídos!")

    except psycopg2.Error as e:
        print(f"Erro ao recriar banco: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def start_docker():
    # Inicia o Docker se USE_DOCKER for True
    if USE_DOCKER:
        print("Iniciando Docker...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)

def stop_docker():
    # Para o Docker se USE_DOCKER for True
    if USE_DOCKER:
        print("Parando Docker...")
        subprocess.run(["docker-compose", "down"], check=True)

def initialize_database():
    conn = None
    cur = None
    try:
        # Conecta como postgres para criar usuários
        conn = get_connection(database="postgres")
        conn.autocommit = True
        cur = conn.cursor()

        create_users(cur)

        cur.close()
        conn.close()

        # Loga como DBA para criar tabelas e índices
        conn = get_connection(database=DB_NAME, user="spacex_dba", password="spacex_dba")
        conn.autocommit = True
        cur = conn.cursor()

        create_tables(cur)
        define_privileges(cur)
        create_indexes(cur)

    except psycopg2.Error as e:
        print(f"Erro ao inicializar banco: {e}")
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("Banco de dados criado!")

if __name__ == "__main__":
    
    start_docker() # Se USE_DOCKER for True
    
    # wait_for_db()
    create_database()
    
    # wait_for_db()
    initialize_database() # Inicializa o banco com tabelas, usuários e índices

    stop_docker() # Se USE_DOCKER for True