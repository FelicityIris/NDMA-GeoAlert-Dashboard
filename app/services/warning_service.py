from pyproj import Geod
from shapely.geometry import Point, Polygon

from app.services.alert_service import get_active_alerts
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
    nearest_point = polygon.boundary.interpolate(polygon.boundary.project(point))
    _, _, distance_m = GEOD.inv(point.x, point.y, nearest_point.x, nearest_point.y)
    return distance_m / 1000

def evaluate_site_against_alert(site, alert):
    point = Point(site["lng"], site["lat"])
    for polygon_string in alert["polygons"]:
        polygon = parse_polygons(polygon_string)
        if polygon.contains(point):
            return { 
                "warning_type": "INSIDE_ALERT_POLYGON", 
                "distance_km": 0
            }
        
        distance_km = distance_to_polygon_km(point, polygon)

        if distance_km <= WARNING_DISTANCE_KM:
            return {
                "warning_type": "NEAR_ALERT_POLYGON",
                "distance_km": round(distance_km, 2)
            }
        
        return None

def generate_warnings():
    warnings = []

    alerts = get_active_alerts()
    project_sites = get_project_sites()
    gnd_sites = get_gnd_sites()

    sites = []

    for site in project_sites:
        sites.append({
            "site_type": "PROJECT",
            "site_name": site["project_name"],
            "lat": site["lat"],
            "lng": site["lng"]
        })

    for site in gnd_sites:
        sites.append({
            "site_type": "GND",
            "site_name": site["site_name"],
            "lat": site["lat"],
            "lng": site["lng"]
        })

    for site in sites:
        for alert in alerts:
            warning = evaluate_site_against_alert(site, alert)
            if warning:
                warnings.append({
                    "site_type": site["site_type"],
                    "site_name": site["site_name"],
                    "alert_id": alert["alert_id"],
                    "alert_identifer": alert["alert_identifier"],
                    "event": alert["event"],
                    "severity": alert["severity"],
                    **warning
                })

    return warnings
