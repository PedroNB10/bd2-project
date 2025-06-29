import requests
from db_connection import get_connection
import psycopg2

def fetch_data(endpoint):
    url = f"https://api.spacexdata.com/v4/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def insert_rockets(data, cur):
    for rocket in data:
        cur.execute(
            """
            INSERT INTO rockets (
                id, name, height, mass, cost_per_launch,
                active, country, description, diameter, first_flight,
                flickr_images, success_rate_pct, wikipedia
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                rocket.get("id"),
                rocket.get("name"),
                rocket.get("height").get("meters"),
                rocket.get("mass").get("kg"),
                rocket.get("cost_per_launch"),
                rocket.get("active"),
                rocket.get("country"),
                rocket.get("description"),
                rocket.get("diameter").get("meters"),
                rocket.get("first_flight"),
                rocket.get("flickr_images")[0],
                rocket.get("success_rate_pct"),
                rocket.get("wikipedia"),
            ),
        )


def insert_launchpads(data, cur):
    for pad in data:
        cur.execute(
            """
            INSERT INTO launchpads (
                id, name, locality, region, status,
                details, full_name, images, latitude, longitude,
                launch_attempts, launch_successes, timezone
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                pad.get("id"),
                pad.get("name"),
                pad.get("locality"),
                pad.get("region"),
                pad.get("status"),
                pad.get("details"),
                pad.get("full_name"),
                pad.get("images").get("large")[0],
                pad.get("latitude"),
                pad.get("longitude"),
                pad.get("launch_attempts"),
                pad.get("launch_successes"),
                pad.get("timezone"),
            ),
        )


def insert_crew(data, cur):
    for member in data:
        cur.execute(
            """
            INSERT INTO crew (
                id, name, status, launch_id,
                agency, image, wikipedia
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                member.get("id"),
                member.get("name"),
                member.get("status"),
                member.get("launches")[0],
                member.get("agency"),
                member.get("image"),
                member.get("wikipedia"),
            ),
        )


def insert_cores(data, cur):
    for core in data:
        cur.execute(
            """
            INSERT INTO cores (
                id, serial, status, reuse_count, asds_attempts,
                asds_landings, rtls_attempts, rtls_landings, last_update
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                core.get("id"),
                core.get("serial"),
                core.get("status"),
                core.get("reuse_count"),
                core.get("asds_attempts"),
                core.get("asds_landings"),
                core.get("rtls_attempts"),
                core.get("rtls_landings"),
                core.get("last_update"),
            ),
        )


def insert_launches(data, cur):
    for launch in data:
        cur.execute(
            """
            INSERT INTO launches (
                id, date_utc, success, rocket_id, launchpad_id,
                details, name
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (
                launch.get("id"),
                launch.get("date_utc"),
                launch.get("success"),
                launch.get("rocket"),
                launch.get("launchpad"),
                launch.get("details"),
                launch.get("name"),
            ),
        )


def insert_starlink_satellites(data, cur):
    for item in data:
        cur.execute(
            """
            INSERT INTO starlink_satellites (
                id, version, launch_id, height_km, latitude, longitude, velocity_kms
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                item.get("id"),
                item.get("version"),
                item.get("launch"),  # Este é o launch_id na tabela
                item.get("height_km"),
                item.get("latitude"),
                item.get("longitude"),
                item.get("velocity_kms"),
            ),
        )


def insert_orbital_parameters(data, cur):
    for item in data:
        space_track = item.get("spaceTrack", {})
        cur.execute(
            """
            INSERT INTO orbital_parameters (
                norad_cat_id, starlink_id, object_id, object_name,
                inclination, eccentricity, semimajor_axis, period,
                mean_motion, apoapsis, periapsis,
                epoch, launch_date,
                decayed,
                creation_date, time_system, classification_type,
                object_type, center_name
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                space_track.get("NORAD_CAT_ID"),
                item.get("id"),  # Chave estrangeira para starlink_satellites
                space_track.get("OBJECT_ID"),
                space_track.get("OBJECT_NAME"),
                space_track.get("INCLINATION"),
                space_track.get("ECCENTRICITY"),
                space_track.get("SEMIMAJOR_AXIS"),
                space_track.get("PERIOD"),
                space_track.get("MEAN_MOTION"),
                space_track.get("APOAPSIS"),
                space_track.get("PERIAPSIS"),
                space_track.get("EPOCH"),
                space_track.get("LAUNCH_DATE"),
                bool(space_track.get("DECAYED")) if space_track else None,
                space_track.get("CREATION_DATE"),
                space_track.get("TIME_SYSTEM"),
                space_track.get("CLASSIFICATION_TYPE"),
                space_track.get("OBJECT_TYPE"),
                space_track.get("CENTER_NAME"),
            ),
        )


def insert_payloads(data, cur):
    for payload in data:
        # AGORA EU TO FAZENDO ISSO COM TRIGGER
        # launch_id = payload.get("launch")
        # cur.execute("SELECT id FROM launches WHERE id = %s", (launch_id,))
        # if not cur.fetchone():
        #     print(f"Launch ID {launch_id} não encontrado. Pulando payload {payload['id']}")
        #     continue
        
        # Tratamento para nationality
        nationalities = payload.get("nationalities", [])
        nationality = nationalities[0] if nationalities else None

        try:
            cur.execute(
                """
                INSERT INTO payloads (
                    id, type, mass_kg, orbit, launch_id,
                    customers, name,
                    nationalities, norad_ids,
                    reference_system, reused, regime
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    payload.get("id"),
                    payload.get("type"),
                    payload.get("mass_kg"),
                    payload.get("orbit"),
                    payload.get("launch"),
                    payload.get("customers"),
                    payload.get("name"),
                    nationality,
                    payload.get("norad_ids"),
                    payload.get("reference_system"),
                    payload.get("reused"),
                    payload.get("regime"),
                ),
            )
            
            # Verifica se há notificações do PostgreSQL
            notices = cur.connection.notices
            if notices:
                for notice in notices:
                    print(notice)  # Mostra a mensagem para o usuário
                cur.connection.notices = []  # Limpa as notificações após exibir
            
        except Exception as e:
            # Se ocorrer algum outro erro (além do trigger)
            print(f"Erro ao inserir payload {payload.get('id')}: {str(e)}")
            continue


def insert_launch_payloads(data, cur):
    for launch in data:
        launch_id = launch.get("id")
        for payload_id in launch.get("payloads", []):
            cur.execute(
                """
                INSERT INTO launch_payloads (launch_id, payload_id)
                VALUES (%s, %s)
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

if __name__ == "__main__":
    run_population()
