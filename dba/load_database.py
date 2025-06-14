import requests
from db_connection import get_connection


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
                rocket.get("height", {}).get("meters"),
                rocket.get("mass", {}).get("kg"),
                rocket.get("cost_per_launch"),
                rocket.get("active"),
                rocket.get("country"),
                rocket.get("description"),
                rocket.get("diameter", {}).get("meters"),
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
                pad.get("images").get("large", [])[0],
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
                details, name, static_fire_date_utc
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                launch.get("id"),
                launch.get("date_utc"),
                launch.get("success"),
                launch.get("rocket"),
                launch.get("launchpad"),
                launch.get("details"),
                launch.get("name"),
                launch.get("static_fire_date_utc"),
            ),
        )


def insert_starlink_satellites(data, cur):
    for item in data:
        space_track = item.get("spaceTrack", {})
        print(space_track.get("DECAYED"))
        cur.execute(
            """
            INSERT INTO starlink_satellites (
                id, height_km, latitude, longitude, velocity_kms, version, launch_id, decayed,
                creation_date, object_id, object_name, center_name, epoch, norad_cat_id,
                time_system, object_type, launch_date, eccentricity, inclination,
                classification_type, apoapsis, periapsis
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                item.get("id"),
                item.get("height_km"),
                item.get("latitude"),
                item.get("longitude"),
                item.get("velocity_kms"),
                item.get("version"),
                item.get("launch"),
                bool(space_track.get("DECAYED")) if space_track else None,
                item.get("spaceTrack", {}).get("CREATION_DATE"),
                item.get("spaceTrack", {}).get("OBJECT_ID"),
                item.get("spaceTrack", {}).get("OBJECT_NAME"),
                item.get("spaceTrack", {}).get("CENTER_NAME"),
                item.get("spaceTrack", {}).get("EPOCH"),
                item.get("spaceTrack", {}).get("NORAD_CAT_ID"),
                item.get("spaceTrack", {}).get("TIME_SYSTEM"),
                item.get("spaceTrack", {}).get("OBJECT_TYPE"),
                item.get("spaceTrack", {}).get("LAUNCH_DATE"),
                item.get("spaceTrack", {}).get("ECCENTRICITY"),
                item.get("spaceTrack", {}).get("INCLINATION"),
                item.get("spaceTrack", {}).get("CLASSIFICATION_TYPE"),
                item.get("spaceTrack", {}).get("APOAPSIS"),
                item.get("spaceTrack", {}).get("PERIAPSIS"),
            ),
        )


def insert_orbital_parameters(data, cur):
    for item in data:
        spaceTrack = item.get("spaceTrack", {})
        cur.execute(
            """
            INSERT INTO orbital_parameters (norad_cat_id, object_name, inclination, semimajor_axis, period,
                                            eccentricity, epoch, mean_motion, starlink_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                item.get("id"),  # O ID da linha que armazena esse dicionário
            ),
        )


def insert_payloads(data, cur):
    for payload in data:
        launch_id = payload.get("launch")
        cur.execute("SELECT id FROM launches WHERE id = %s", (launch_id,))
        if not cur.fetchone():
            print(f"Launch ID {launch_id} não encontrado. Pulando payload {payload['id']}")
            continue
        
        # Tratamento para nationality
        nationalities = payload.get("nationalities", [])
        nationality = nationalities[0] if nationalities else None

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
                payload.get("customers", []),
                payload.get("name"),
                nationality,
                payload.get("norad_ids", []),
                payload.get("reference_system"),
                payload.get("reused"),
                payload.get("regime"),
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
