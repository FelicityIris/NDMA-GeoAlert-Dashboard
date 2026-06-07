from flask import Blueprint, jsonify, render_template

from app.services.alert_service import get_alert_by_id, get_all_alerts, get_polygon_data
from app.services.site_service import get_gnd_sites, get_project_sites
from app.services.warning_service import get_all_warnings, get_project_warnings

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    alerts = get_all_alerts()
    polygon_data = get_polygon_data()
    project_sites = get_project_sites()
    gnd_sites = get_gnd_sites()
    projects = get_all_warnings()

    return render_template(
        "public/index.html",
        alerts=alerts,
        polygon_data=polygon_data,
        project_sites=project_sites,
        gnd_sites=gnd_sites,
        projects=projects
    )

@public_bp.route("/alert/<int:alert_id>")
def alert_by_id(alert_id):
    alert = get_alert_by_id(alert_id)
    if not alert:
        return jsonify({"error": "Alert not found"}), 404
    return jsonify(alert)

@public_bp.route("/warnings")
def warnings():
    return jsonify(get_all_warnings())

@public_bp.route("/warnings/project/<int:project_id>")
def project_warnings(project_id):
    warnings = get_project_warnings(project_id)
    return jsonify(warnings)
