from collections import defaultdict

from pyproj import Geod
from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points

from app.services.alert_service import get_active_alerts
from app.services.db import get_connection
from app.services.site_service import get_gnd_sites, get_project_sites

GEOD = Geod(ellps="WGS84")

WARNING_DISTANCE_KM = 50


def parse_polygons(polygon_string):
    coordinates = polygon_string.strip().split()

    points = []

    for coordinate in coordinates:
        lat, lng = map(float, coordinate.split(","))
        points.append((lng, lat))
    return Polygon(points)


def distance_to_polygon_km(point, polygon):
    nearest_geom, _ = nearest_points(polygon.boundary, point)
    _, _, distance_m = GEOD.inv(point.x, point.y, nearest_geom.x, nearest_geom.y)
    return distance_m / 1000


def evaluate_site_against_alert(site, alert):
    point = Point(site["lng"], site["lat"])

    nearest_distance = None

    for polygon_string in alert["polygons"]:
        polygon = parse_polygons(polygon_string)

        if polygon.contains(point):
            return {"warning_type": "INSIDE_ALERT_POLYGON", "distance_km": 0}

        distance_km = distance_to_polygon_km(point, polygon)

        if nearest_distance is None or distance_km < nearest_distance:
            nearest_distance = distance_km

    if nearest_distance is not None and nearest_distance <= WARNING_DISTANCE_KM:
        return {
            "warning_type": "NEAR_ALERT_POLYGON",
            "distance_km": round(nearest_distance, 2),
        }

    return None


def generate_warnings():
    warnings = []

    alerts = get_active_alerts()
    project_sites = get_project_sites()
    gnd_sites = get_gnd_sites()

    project_lookup = {}

    for project in project_sites:
        project_lookup[project["project_id"]] = project

    sites = []

    for site in project_sites:
        sites.append(
            {
                "site_type": "PROJECT",
                "site_name": site["project_name"],
                "project_id": site["project_id"],
                "lat": site["lat"],
                "lng": site["lng"],
            }
        )

    for site in gnd_sites:
        sites.append(
            {
                "site_type": "GND",
                "site_name": site["site_name"],
                "project_id": site["project_id"],
                "lat": site["lat"],
                "lng": site["lng"],
            }
        )

    best_warnings = {}

    for site in sites:
        for alert in alerts:
            warning = evaluate_site_against_alert(site, alert)

            if not warning:
                continue

            if site["site_type"] == "PROJECT":
                warning_site_name = site["site_name"]
            else:
                project = project_lookup.get(site["project_id"])

                if not project:
                    continue

                warning_site_name = project["project_name"]

            warning_key = (warning_site_name, alert["alert_id"])

            candidate = {
                "site_type": site["site_type"],
                "site_name": warning_site_name,
                "project_id": site["project_id"],
                "alert_id": alert["alert_id"],
                "event": alert["event"],
                "severity": alert["severity"],
                **warning,
            }

            existing = best_warnings.get(warning_key)
            if existing is None or candidate["distance_km"] < existing["distance_km"]:
                best_warnings[warning_key] = candidate

    return list(best_warnings.values())


def refresh_warnings():
    warnings = generate_warnings()
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM warnings")
            for warning in warnings:
                cursor.execute(
                    """
                        INSERT INTO warnings (
                            alert_id,
                            site_type,
                            site_name,
                            project_id,
                            warning_type,
                            distance_km
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        warning["alert_id"],
                        warning["site_type"],
                        warning["site_name"],
                        warning["project_id"],
                        warning["warning_type"],
                        warning["distance_km"],
                    ),
                )
        print("Warnings regenerated and stored in DB")
        connection.commit()
    except Exception as error_msg:
        print(f"Error: Failed to regenerate warnings")
        print(error_msg)
    finally:
        connection.close()


def get_all_warnings():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT
                        warnings.alert_id,
                        warnings.site_name,
                        warnings.project_id,
                        warnings.warning_type,
                        warnings.distance_km,

                        alerts.event,
                        alerts.severity,
                        alerts.expires
                    FROM warnings
                    JOIN alerts
                        ON warnings.alert_id = alerts.alert_id
                    ORDER BY
                        warnings.distance_km
                """)
            warnings = cursor.fetchall()

        projects = {}

        for warning in warnings:
            project_id = warning["project_id"]
            project_name = warning["site_name"]

            if project_name not in projects:
                projects[project_name] = {
                    "project_id": project_id,
                    "project_name": project_name,
                    "alerts": [],
                }

            projects[project_name]["alerts"].append(
                {
                    "alert_id": warning["alert_id"],
                    "event": warning["event"],
                    "severity": warning["severity"],
                    "expires": warning["expires"],
                    "warning_type": warning["warning_type"],
                    "distance_km": warning["distance_km"],
                }
            )

        return sorted(
            projects.values(), key=lambda project: len(project["alerts"]), reverse=True
        )
    finally:
        connection.close()


def get_project_warnings(project_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    project_id,
                    project_name
                FROM project_sites
                WHERE project_id = %s
                """,
                (project_id,)
            )
            project = cursor.fetchone()

            if not project:
                return {
                    "project_exists": False,
                    "message": "No associated project site in database."
                }

            cursor.execute(
                """
                SELECT
                    warnings.alert_id,
                    warnings.project_id,
                    warnings.site_name,
                    warnings.warning_type,
                    warnings.distance_km,

                    alerts.event,
                    alerts.severity,
                    alerts.expires

                FROM warnings

                JOIN alerts
                    ON warnings.alert_id = alerts.alert_id

                WHERE
                    warnings.project_id = %s

                ORDER BY
                    warnings.distance_km
                """,
                (project_id,)
            )

            warnings = cursor.fetchall()

            if not warnings:
                return {
                    "project_exists": True,
                    "project": project,
                    "message": "No active alerts affecting this project site."
                }
            
            return {
                "project_exists": True,
                "project": project,
                "warning_count": len(warnings),
                "warnings": warnings
            }
    finally:
        connection.close()


def get_projects_by_alerts():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    alert_id,
                    project_id,
                    site_name
                FROM warnings
                ORDER BY site_name
                """)
            rows = cursor.fetchall()

        projects_by_alert = defaultdict(list)
        for row in rows:
            projects_by_alert[row["alert_id"]].append(
                {"project_id": row["project_id"], "project_name": row["site_name"]}
            )

        return projects_by_alert
    finally:
        connection.close()
