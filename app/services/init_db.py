import csv
from pathlib import Path
from app.services.db import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "database" / "data"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

def execute_schema():
    connection = get_connection(database = False)

    try:
        with connection.cursor() as cursor:
            with open(SCHEMA_PATH, "r", encoding = "utf-8") as file:
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
    with open(DATA_DIR / "states.csv", newline = "", encoding = "utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = """
                INSERT IGNORE INTO states (state_name, feed_slug)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (row["state_name"], row["feed_slug"]))

def seed_districts(cursor):
    with open(DATA_DIR / "districts.csv", newline = "", encoding = "utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sql = """
                INSERT IGNORE INTO districts (district_code, district_name)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (int(row["district_code"]), row["district_name"]))

def seed_database():
    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            if table_is_empty(cursor, "states"):
                print("Seeding states...")
                seed_states(cursor)
            if table_is_empty(cursor, "districts"):
                print("Seeding districts...")
                seed_districts(cursor)
        connection.commit()
    finally:
        connection.close()

def initialize_database():
    execute_schema()
    seed_database()
    print("Database initialization complete.")