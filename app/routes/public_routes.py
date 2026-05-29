from flask import Blueprint, jsonify, render_template

from app.services.alert_service import get_all_alerts, get_polygon_data
from app.services.site_service import get_gnd_sites, get_project_sites
from app.services.warning_service import generate_warnings

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    alerts = get_all_alerts()
    polygon_data = get_polygon_data()
    project_sites = get_project_sites()
    gnd_sites = get_gnd_sites()

    return render_template(
        "public/index.html",
        alerts=alerts,
        polygon_data=polygon_data,
        project_sites=project_sites,
        gnd_sites=gnd_sites
    )

@public_bp.route("/warnings")
def warnings():
    return jsonify(generate_warnings())
