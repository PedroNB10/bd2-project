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

-- CARGAS ÚTEIS
CREATE TABLE PAYLOADS (
    id VARCHAR PRIMARY KEY,
    type VARCHAR,
    mass_kg FLOAT,
    orbit VARCHAR
);

-- TRIPULAÇÃO
CREATE TABLE CREW (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    status VARCHAR
);

-- NÚCLEOS (CORES)
CREATE TABLE CORES (
    id VARCHAR PRIMARY KEY,
    reused BOOLEAN,
    land_success BOOLEAN
);

-- MISSÕES
CREATE TABLE MISSIONS (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    description VARCHAR
);

-- LANÇAMENTOS
CREATE TABLE LAUNCHES (
    id VARCHAR PRIMARY KEY,
    date_utc DATETIME,
    success BOOLEAN,
    rocket_id VARCHAR,
    launchpad_id VARCHAR,
    FOREIGN KEY (rocket_id) REFERENCES ROCKETS(id),
    FOREIGN KEY (launchpad_id) REFERENCES LAUNCHPADS(id)
);

-- Relação N:N entre LANÇAMENTOS e CARGAS
CREATE TABLE LAUNCH_PAYLOADS (
    launch_id VARCHAR,
    payload_id VARCHAR,
    PRIMARY KEY (launch_id, payload_id),
    FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id),
    FOREIGN KEY (payload_id) REFERENCES PAYLOADS(id)
);

-- Relação N:N entre LANÇAMENTOS e TRIPULAÇÃO
CREATE TABLE LAUNCH_CREW (
    launch_id VARCHAR,
    crew_id VARCHAR,
    PRIMARY KEY (launch_id, crew_id),
    FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id),
    FOREIGN KEY (crew_id) REFERENCES CREW(id)
);

-- Relação N:N entre LANÇAMENTOS e NÚCLEOS
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

-- Relação N:N entre MISSÕES e LANÇAMENTOS
CREATE TABLE MISSION_LAUNCHES (
    mission_id VARCHAR,
    launch_id VARCHAR,
    PRIMARY KEY (mission_id, launch_id),
    FOREIGN KEY (mission_id) REFERENCES MISSIONS(id),
    FOREIGN KEY (launch_id) REFERENCES LAUNCHES(id)
);

-- Relação N:N entre MISSÕES e CARGAS
CREATE TABLE MISSION_PAYLOADS (
    mission_id VARCHAR,
    payload_id VARCHAR,
    PRIMARY KEY (mission_id, payload_id),
    FOREIGN KEY (mission_id) REFERENCES MISSIONS(id),
    FOREIGN KEY (payload_id) REFERENCES PAYLOADS(id)
);
