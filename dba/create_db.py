from db_connection import get_connection
import psycopg2
from backend.config import DB_NAME

from create_indexes import create_indexes
from users_and_privileges import create_users, define_privileges
from create_tables import create_tables
from create_triggers import create_trigger_payload

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
        create_trigger_payload(cur)
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
    create_database()
    
    initialize_database() # Inicializa o banco com tabelas, usuários e índices