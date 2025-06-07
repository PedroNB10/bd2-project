from db_connection import get_connection, wait_for_db
import subprocess
from backend.config import USE_DOCKER
import psycopg2
from backend.config import DB_NAME

from create_indexes import create_indexes
from create_users import create_users
from create_tables import create_tables

def create_database():
    try:
        # Conecta ao banco postgres, pois o banco pode não existir
        conn = get_connection("postgres")
        conn.autocommit = True
        cur = conn.cursor()

        # Encerra o processo relacionado ao banco que está sendo criado caso tenha
        # Para permitir que o código rode sem que o usuário precise encerrar a sessão manualmente
        cur.execute(
            f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{DB_NAME}';
            """
        )

        # Remove banco antigo (se tiver) e recria banco novo
        cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Banco {DB_NAME} recriado!")
        
    except psycopg2.Error as e:
        print(f"Erro ao recriar banco: {e}")
        raise
    finally:
        cur.close()
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
    try:
        conn = get_connection(DB_NAME)
        conn.autocommit = True
        cur = conn.cursor()
        
        create_tables(cur)         
        create_users(cur)
        create_indexes(cur)
        
    except psycopg2.Error as e:
        print(f"Erro ao inicializar banco: {e}")
        raise
    
    finally:
        cur.close()
        conn.close()
        print("Banco de dados criado!")

if __name__ == "__main__":
    
    start_docker() # Se USE_DOCKER for True
    
    wait_for_db()
    create_database()
    
    wait_for_db()
    initialize_database() # Inicializa o banco com tabelas, usuários e índices

    stop_docker() # Se USE_DOCKER for True