import pymysql
import os

def get_connection(database = True):
    connection_config = {
        "host" : os.getenv("DB_HOST"),
        "user" : os.getenv("DB_USER"),
        "password" : os.getenv("DB_PASSWORD"),
        "cursorclass" : pymysql.cursors.DictCursor
    }

    if database:
        connection_config["database"] = os.getenv("DB_NAME")

    return pymysql.connect(**connection_config)