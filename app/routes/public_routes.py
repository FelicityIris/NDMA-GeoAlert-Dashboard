from flask import ( Blueprint, render_template )
from app.services.alert_service import ( get_all_alerts, get_polygon_data )
from app.services.ingestion_service import ingest_alerts

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    alerts = get_all_alerts()
    polygon_data = get_polygon_data()
    return render_template("public/index.html", alerts = alerts, polygon_data = polygon_data)