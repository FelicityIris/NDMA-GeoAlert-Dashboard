from app.services.db import get_connection

def get_all_alerts():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT *
                FROM alerts
                ORDER BY effective DESC
            """

            cursor.execute(sql)

            alerts = cursor.fetchall()

            return alerts
    finally:
        connection.close()