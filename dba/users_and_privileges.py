def create_users(cur):
    try:
        # Criando usuários (DBA como SUPERUSER)
            # 1. spacex_dba
            # 2. spacex_api
            # 3. spacex_app (pode ser separado futuramente em mais usuários, definindo uma role para ela)
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'spacex_dba'")
        if not cur.fetchone():
            cur.execute("CREATE USER spacex_dba WITH PASSWORD 'spacex_dba' SUPERUSER")
        
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'spacex_api'")
        if not cur.fetchone():
            cur.execute("CREATE USER spacex_api WITH PASSWORD 'spacex_api'")
        
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'spacex_app'")
        if not cur.fetchone():
            cur.execute("CREATE USER spacex_app WITH PASSWORD 'spacex_app'")
            
        # O privilégio do DBA deve ser definido aqui
        cur.execute("GRANT ALL PRIVILEGES ON DATABASE spacex_bd2 TO spacex_dba")

        print("Usuários criados!")
        return True
        
    except Exception as e:
        print(f"Falha ao criar usuários: {e}")
        cur.execute("ROLLBACK")
        return False
    
def define_privileges(cur):
    try:
        
    # Definindo privilégios (Menos o DBA q foi definido na função de criação dos usuários)
        cur.execute("""
            GRANT CONNECT ON DATABASE spacex_bd2 TO spacex_api, spacex_app;
            GRANT USAGE ON SCHEMA public TO spacex_api, spacex_app;
            GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA public TO spacex_api;
            GRANT SELECT ON ALL TABLES IN SCHEMA public TO spacex_app;
        """)
        
    except Exception as e:
        print(f"Falha ao definir privilégios: {e}")
        cur.execute("ROLLBACK")
        return False