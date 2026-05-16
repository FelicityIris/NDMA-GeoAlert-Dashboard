from flask import Blueprint, render_template

from app.services.alert_service import get_all_alerts

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    alerts = get_all_alerts()

    return render_template("public/index.html", alerts = alerts)