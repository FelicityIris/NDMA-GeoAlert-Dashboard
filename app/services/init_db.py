import pymysql
import os

def initialize_database():
    connection = pymysql.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )

    try:
        with connection.cursor() as cursor:
            with open("database/schema.sql", "r") as file:
                sql_script = file.read()
            
            queries = sql_script.split(";")

            for query in queries:
                query = query.strip()

                if query:
                    cursor.execute(query)
        connection.commit()
    finally:
        connection.close()