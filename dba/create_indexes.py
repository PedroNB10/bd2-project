def create_indexes(cur):
    # A consulta abaixo foi usada para ajudar a definir onde os índices seriam inseridos
    '''
    Retorna a quantidade de linhas em todas as colunas do banco:

    SELECT 
        relname AS table_name, 
        n_live_tup AS total_rows
    FROM 
        pg_stat_user_tables
    ORDER BY 
        total_rows DESC;
    '''    
        
    try:
        # Índices para tabela launches (pois possui vários relacionamentos)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_launches_date ON launches(date_utc)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_launches_success ON launches(success)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_launches_rocket ON launches(rocket_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_launches_launchpad ON launches(launchpad_id)")
        
        # Índices para relacionamentos
        cur.execute("CREATE INDEX IF NOT EXISTS idx_payloads_launch ON payloads(launch_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_starlink_launch ON starlink_satellites(launch_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_orbital_starlink ON orbital_parameters(starlink_id)")
        
        print("Índices criados com sucesso!")
        return True
        
    except Exception as e:
        print(f"Falha ao criar índices: {e}")
        return False