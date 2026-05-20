from app.services.db import get_connection

def get_selected_states():
    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT state_id, state_name, feed_slug
                FROM states
                WHERE is_selected = TRUE
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()