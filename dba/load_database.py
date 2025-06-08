import subprocess
import requests
from db_connection import get_connection, wait_for_db
from backend.config import USE_DOCKER


def fetch_data(endpoint):
    url = f"https://api.spacexdata.com/v4/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def insert_rockets(data, cur):
    for rocket in data:
        cur.execute(
            """
            INSERT INTO rockets (id, name, height, mass, cost_per_launch)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                rocket.get("id"),
                rocket.get("name"),
                rocket.get("height", {}).get("meters"),
                rocket.get("mass", {}).get("kg"),
                rocket.get("cost_per_launch"),
            ),
        )


def insert_launchpads(data, cur):
    for pad in data:
        cur.execute(
            """
            INSERT INTO launchpads (id, name, locality, region, status)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                pad.get("id"),
                pad.get("name"),
                pad.get("locality"),
                pad.get("region"),
                pad.get("status"),
            ),
        )


def insert_crew(data, cur):
    for member in data:
        cur.execute(
            """
            INSERT INTO crew (id, name, status, launch_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                member.get("id"),
                member.get("name"),
                member.get("status"),
                member.get("launches")[0],
            ),
        )


def insert_cores(data, cur):
    for core in data:
        core_id = core.get("id")
        if core_id is None:
            continue
        cur.execute(
            """
            INSERT INTO cores (id, serial, status, reuse_count, asds_attempts, asds_landings, rtls_attempts, rtls_landings)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                core_id,
                core.get("serial"),
                core.get("status"),
                core.get("reuse_count", 0),
                core.get("asds_attempts", 0),
                core.get("asds_landings", 0),
                core.get("rtls_attempts", 0),
                core.get("rtls_landings", 0),
            ),
        )


def insert_launches(data, cur):
    for launch in data:
        cur.execute(
            """
            INSERT INTO launches (id, date_utc, success, rocket_id, launchpad_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                launch.get("id"),
                launch.get("date_utc"),
                launch.get("success"),
                launch.get("rocket"),
                launch.get("launchpad"),
            ),
        )


def insert_starlink_satellites(data, cur):
    for item in data:
        cur.execute(
            """
            INSERT INTO starlink_satellites (id, height_km, latitude, longitude, velocity_kms, version, launch_id, decayed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                item.get("id"),
                item.get("height_km"),
                item.get("latitude"),
                item.get("longitude"),
                item.get("velocity_kms"),
                item.get("version"),
                item.get("launch"),  # Aqui está a correção
                (
                    bool(item.get("spaceTrack", {}).get("DECAYED"))
                    if item.get("spaceTrack")
                    else None
                ),
            ),
        )


def insert_orbital_parameters(data, cur):
    for item in data:
        spaceTrack = item.get("spaceTrack", {})
        cur.execute(
            """
            INSERT INTO orbital_parameters (norad_cat_id, object_name, inclination, semimajor_axis, period,
                                            eccentricity, epoch, mean_motion, country_code, starlink_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (norad_cat_id) DO NOTHING;
        """,
            (
                spaceTrack.get("NORAD_CAT_ID"),
                spaceTrack.get("OBJECT_NAME"),
                spaceTrack.get("INCLINATION"),
                spaceTrack.get("SEMIMAJOR_AXIS"),
                spaceTrack.get("PERIOD"),
                spaceTrack.get("ECCENTRICITY"),
                spaceTrack.get("EPOCH"),
                spaceTrack.get("MEAN_MOTION"),
                spaceTrack.get("COUNTRY_CODE"),
                item.get("id"),  # O ID da linha que armazena esse dicionário
            ),
        )


def insert_payloads(data, cur):
    for payload in data:
        launch_id = payload.get("launch")

        # Verifique se o launch_id existe em launches
        # Essa etapa é necessária pois tem launch_is em payload q n n existe na tabela launches
        cur.execute("SELECT id FROM launches WHERE id = %s", (launch_id,))
        if not cur.fetchone():
            print(
                f"Launch ID {launch_id} não encontrado. Pulando payload {payload['id']}"
            )
            continue  # Ignora este payload

        cur.execute(
            """
            INSERT INTO payloads (id, type, mass_kg, orbit, launch_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (
                payload.get("id"),
                payload.get("type"),
                payload.get("mass_kg"),
                payload.get("orbit"),
                payload.get("launch"),
            ),
        )


def insert_launch_payloads(data, cur):
    for launch in data:
        launch_id = launch.get("id")
        for payload_id in launch.get("payloads", []):
            cur.execute(
                """
                INSERT INTO launch_payloads (launch_id, payload_id)
                VALUES (%s, %s)
                ON CONFLICT (launch_id, payload_id) DO NOTHING;
            """,
                (launch_id, payload_id),
            )


def insert_launch_cores(data, cur):
    for launch in data:
        launch_id = launch.get("id")
        for core in launch.get("cores", []):
            core_id = core.get("core")
            if core_id is None:
                continue  # pula se não houver core associado
            cur.execute(
                """
                INSERT INTO launch_cores (launch_id, core_id, flight_number, reused, land_success)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (launch_id, core_id) DO NOTHING;
            """,
                (
                    launch_id,
                    core_id,
                    core.get("flight"),
                    core.get("reused"),
                    core.get("landing_success"),
                ),
            )


def run_population():
    try:
        if USE_DOCKER:
            print("Starting Docker Compose...")
            subprocess.run(["docker", "compose", "up", "-d"], check=True)

        wait_for_db()

        conn = get_connection(database="spacex_bd2", user="spacex_api", password="spacex_api")
        cur = conn.cursor()

        rockets = fetch_data("rockets")
        launchpads = fetch_data("launchpads")
        crew = fetch_data("crew")
        cores = fetch_data("cores")
        launches = fetch_data("launches")
        starlink_data = fetch_data("starlink")
        payloads = fetch_data("payloads")

        insert_rockets(rockets, cur)
        insert_launchpads(launchpads, cur)
        insert_cores(cores, cur)
        insert_launches(launches, cur)
        insert_crew(crew, cur)

        starlink_data = fetch_data("starlink")

        insert_starlink_satellites(starlink_data, cur)
        insert_orbital_parameters(starlink_data, cur)
        insert_payloads(payloads, cur)

        insert_launch_payloads(launches, cur)
        insert_launch_cores(launches, cur)

        conn.commit()
        cur.close()
        conn.close()
        print("Dados e relacionamentos inseridos com sucesso.")

    except KeyboardInterrupt:
        print("Application interrupted by user.")
    finally:
        if USE_DOCKER:
            print("Stopping Docker Compose...")
            subprocess.run(["docker", "compose", "down"], check=True)


if __name__ == "__main__":
    run_population()
