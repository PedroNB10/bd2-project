def create_tables(cur):
    try:
        cur.execute(
            """
                -- FOGUETES
                CREATE TABLE ROCKETS (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR,
                    height FLOAT,
                    mass FLOAT,
                    cost_per_launch FLOAT
                );

                -- PLATAFORMAS DE LANÇAMENTO
                CREATE TABLE LAUNCHPADS (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR,
                    locality VARCHAR,
                    region VARCHAR,
                    status VARCHAR
                );

                -- LANÇAMENTOS
                CREATE TABLE LAUNCHES (
                    id VARCHAR PRIMARY KEY,
                    date_utc TIMESTAMP,
                    success BOOLEAN,
                    rocket_id VARCHAR,
                    launchpad_id VARCHAR,
                    FOREIGN KEY (rocket_id) REFERENCES ROCKETS(id),
                    FOREIGN KEY (launchpad_id) REFERENCES LAUNCHPADS(id)
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
                    country_code VARCHAR(3),
                    starlink_id VARCHAR NOT NULL,
                    FOREIGN KEY (starlink_id) REFERENCES STARLINK_SATELLITES(id)
                );

                -- CARGAS ÚTEIS
                CREATE TABLE payloads (
                    id VARCHAR PRIMARY KEY,
                    type VARCHAR,
                    mass_kg FLOAT,
                    orbit VARCHAR,
                    launch_id VARCHAR NOT NULL,
                    FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id)
                );


                -- TRIPULAÇÃO
                CREATE TABLE CREW (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR,
                    status VARCHAR,
                    launch_id VARCHAR,
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
                    rtls_landings INT
                );


                -- LANÇAMENTOS <-> CARGAS
                CREATE TABLE LAUNCH_PAYLOADS (
                    launch_id VARCHAR,
                    payload_id VARCHAR,
                    PRIMARY KEY (launch_id, payload_id),
                    FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id),
                    FOREIGN KEY (payload_id) REFERENCES PAYLOADS(id)
                );

                -- LANÇAMENTOS <-> NÚCLEOS
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
            """
        )
    except Exception as e:
        print(f"Falha ao criar tabelas: {e}")
        return False