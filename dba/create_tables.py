def create_tables(cur):
    try:
        cur.execute(
            '''
            -- FOGUETES
            CREATE TABLE ROCKETS (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                height FLOAT,
                mass FLOAT,
                cost_per_launch FLOAT,
                
                -- Adicionado depois da reunião
                active BOOLEAN,
                country VARCHAR,
                description TEXT,
                diameter FLOAT,
                first_flight DATE,
                flickr_images TEXT[], -- Array de URLs de imagens
                success_rate_pct INT,
                wikipedia VARCHAR
            );

            -- PLATAFORMAS DE LANÇAMENTO
            CREATE TABLE LAUNCHPADS (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                locality VARCHAR,
                region VARCHAR,
                status VARCHAR,
                
                -- Adicionado depois da reunião
                details TEXT,
                full_name VARCHAR,
                images TEXT[], -- Array de URLs de imagens
                latitude FLOAT,
                longitude FLOAT,
                launch_attempts INT,
                launch_successes INT,
                timezone VARCHAR
            );

            -- LANÇAMENTOS
            CREATE TABLE LAUNCHES (
                id VARCHAR PRIMARY KEY,
                date_utc TIMESTAMP,
                success BOOLEAN,
                rocket_id VARCHAR,
                launchpad_id VARCHAR,
                
                -- Adicionado depois da reunião
                details TEXT,
                name VARCHAR,
                static_fire_date_utc TIMESTAMP,
                
                FOREIGN KEY (launchpad_id) REFERENCES LAUNCHPADS(id),
                FOREIGN KEY (rocket_id) REFERENCES ROCKETS(id)
            );
            
            -- STARLINK SATÉLITES
            CREATE TABLE starlink_satellites (
                id VARCHAR PRIMARY KEY,
                height_km FLOAT,
                latitude FLOAT,
                longitude FLOAT,
                velocity_kms FLOAT,
                version VARCHAR,
                launch_id VARCHAR NULL,  -- Relação N:1 com launches
                decayed BOOLEAN,
                
                -- Adicionado depois da reunião
                creation_date TIMESTAMP,
                object_id VARCHAR,
                object_name VARCHAR,
                center_name VARCHAR,
                epoch TIMESTAMP,
                norad_cat_id INT,
                time_system VARCHAR,
                object_type VARCHAR,
                launch_date TIMESTAMP,
                decay_date TIMESTAMP,
                eccentricity FLOAT,
                inclination FLOAT,
                classification_type VARCHAR,
                apoapsis FLOAT,
                periapsis FLOAT,
                
                FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id)
            );

            -- PARÂMETROS ORBITAIS
            CREATE TABLE ORBITAL_PARAMETERS (
                norad_cat_id INT PRIMARY KEY,
                object_name VARCHAR,
                inclination FLOAT,
                semimajor_axis FLOAT,
                period FLOAT,
                eccentricity FLOAT,
                epoch TIMESTAMP,
                mean_motion FLOAT,
                starlink_id VARCHAR NOT NULL,
                FOREIGN KEY (starlink_id) REFERENCES STARLINK_SATELLITES(id)
            );

            -- CARGAS ÚTEIS
            CREATE TABLE payloads (
                id VARCHAR PRIMARY KEY,
                type VARCHAR,
                mass_kg FLOAT,
                orbit VARCHAR,
                launch_id VARCHAR,
                
                -- Adicionado depois da reunião
                apoapsis_km FLOAT,
                arg_of_pericenter FLOAT,
                customers TEXT[], -- Array de clientes
                eccentricity FLOAT,
                epoch TIMESTAMP,
                name VARCHAR,
                nationalities TEXT,
                norad_ids INT[], -- Array de IDs NORAD
                periapsis_km FLOAT,
                reference_system VARCHAR,
                reused BOOLEAN,
                regime VARCHAR,
                
                FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id)
            );

            -- TRIPULAÇÃO
            CREATE TABLE CREW (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                status VARCHAR,
                launch_id VARCHAR,
                
                -- Adicionado depois da reunião
                agency VARCHAR,
                image VARCHAR, -- URL da imagem
                wikipedia VARCHAR,
                
                FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id)
            );

            -- NÚCLEOS
            CREATE TABLE cores (
                id VARCHAR PRIMARY KEY,
                serial VARCHAR,
                status VARCHAR,
                reuse_count INT,
                asds_attempts INT,
                asds_landings INT,
                rtls_attempts INT,
                rtls_landings INT,
                
                -- Adicionado depois da reunião
                last_update TEXT
            );

            -----------------------------------------------------------
            -- Tabelas de relacionamento mantidas conforme necessidade
            -----------------------------------------------------------
            CREATE TABLE LAUNCH_PAYLOADS (
                launch_id VARCHAR,
                payload_id VARCHAR,
                PRIMARY KEY (launch_id, payload_id),
                FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id),
                FOREIGN KEY (payload_id) REFERENCES PAYLOADS(id)
            );

            CREATE TABLE LAUNCH_CORES (
                launch_id VARCHAR,
                core_id VARCHAR,
                flight_number INT,
                reused BOOLEAN,
                land_success BOOLEAN,
                PRIMARY KEY (launch_id, core_id),
                FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id),
                FOREIGN KEY (core_id) REFERENCES CORES(id)
            );
            
            '''
        )
    except Exception as e:
        print(f"Falha ao criar tabelas: {e}")
        return False