import psycopg2

def get_connection(database="postgres"):
    return psycopg2.connect(
        host="IP",
        port=5432,
        database=database,
        user="postgres",
        password="senha"
    )
