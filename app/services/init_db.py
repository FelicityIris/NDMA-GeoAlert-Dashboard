import csv
from pathlib import Path

from app.services.db import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "database" / "data"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def execute_schema():
    connection = get_connection(database=False)

    try:
        with connection.cursor() as cursor:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
                sql_script = file.read()

            queries = sql_script.split(";")

            for query in queries:
                query = query.strip()

                if query:
                    cursor.execute(query)
        connection.commit()
    finally:
        connection.close()


def table_is_empty(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) AS count FROM {table_name}")
    result = cursor.fetchone()
    return result["count"] == 0


def seed_states(cursor):
    with open(DATA_DIR / "states.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = """
                INSERT IGNORE INTO states (state_name, feed_slug)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (row["state_name"], row["feed_slug"]))


def seed_districts(cursor):
    with open(DATA_DIR / "districts.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = """
                INSERT IGNORE INTO districts (district_code, district_name)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (int(row["district_code"]), row["district_name"]))


def seed_gnd_sites(cursor):
    with open(DATA_DIR / "gnd_sites.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = """
                INSERT IGNORE INTO gnd_sites (site_name, project_id, lat, lng)
                VALUES (%s, %s, %s, %s)
            """

            project_id = None
            if row["project_id"] != "NULL":
                project_id = int(row["project_id"])

            if (row["lat"] == "NULL") or (row["lng"] == "NULL"):
                continue

            cursor.execute(
                sql,
                (
                    row["site_name"],
                    project_id,
                    float(row["lat"]),
                    float(row["lng"]),
                ),
            )


def seed_project_sites(cursor):
    with open(DATA_DIR / "project_sites.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = """
                INSERT IGNORE INTO project_sites (project_id, project_name, lat, lng)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    int(row["project_id"]),
                    row["project_name"],
                    float(row["lat"]),
                    float(row["lng"]),
                ),
            )


def seed_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            if table_is_empty(cursor, "states"):
                print("Seeding States Data...")
                seed_states(cursor)
            if table_is_empty(cursor, "districts"):
                print("Seeding Districts Data...")
                seed_districts(cursor)
            if table_is_empty(cursor, table_name="gnd_sites"):
                print("Seeding GND Sites Data...")
                seed_gnd_sites(cursor)
            if table_is_empty(cursor, table_name="project_sites"):
                print("Seeding Project Sites Data...")
                seed_project_sites(cursor)
        connection.commit()
    finally:
        connection.close()


def initialize_database():
    execute_schema()
    seed_database()
    print("Database initialization complete.")
