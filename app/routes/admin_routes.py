from flask import ( Blueprint, render_template, request, redirect, url_for )
from app.services.state_service import ( get_all_states, update_selected_states )
from app.services.ingestion_service import ingest_alerts

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_dashboard():
    states = get_all_states()
    return render_template("admin/dashboard.html", states = states)

@admin_bp.route("/admin/states", methods = ["POST"])
def update_states():
    selected_states = request.form.getlist("selected_states")
    selected_states = [int(state_id) for state_id in selected_states]
    update_selected_states(selected_states)
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/ingest")
def admin_ingest():
    ingest_alerts()
    return redirect(url_for("admin.admin_dashboard"))