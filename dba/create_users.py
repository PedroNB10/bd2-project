def create_users(cur):
    '''
    Excluir usuários criados no banco:
    
    DROP OWNED BY spacex_dba CASCADE;
    DROP OWNED BY spacex_api CASCADE;
    DROP OWNED BY spacex_app CASCADE;

    DROP ROLE IF EXISTS spacex_dba;
    DROP ROLE IF EXISTS spacex_api;
    DROP ROLE IF EXISTS spacex_app;
    '''
    
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

        # Definindo privilégios
        cur.execute("""
            GRANT ALL PRIVILEGES ON DATABASE spacex_bd2 TO spacex_dba;
            GRANT CONNECT ON DATABASE spacex_bd2 TO spacex_api, spacex_app;
            GRANT USAGE ON SCHEMA public TO spacex_api, spacex_app;
            GRANT INSERT ON ALL TABLES IN SCHEMA public TO spacex_api;
            GRANT SELECT ON ALL TABLES IN SCHEMA public TO spacex_app;
        """)

        print("Usuários e permissões configurados com sucesso!")
        return True
        
    except Exception as e:
        print(f"Falha ao criar usuários: {e}")
        cur.execute("ROLLBACK")
        return False