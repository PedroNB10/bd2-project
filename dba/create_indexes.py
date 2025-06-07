def create_indexes(cur):
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