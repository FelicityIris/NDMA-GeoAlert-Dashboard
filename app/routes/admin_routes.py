from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.auth.auth_service import validate_admin_login
from app.services.ingestion_service import ingest_alerts
from app.services.state_service import get_all_states, update_selected_states

admin_bp = Blueprint("admin", __name__)


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.admin_login"))

        return view(*args, **kwargs)

    return wrapped_view


@admin_bp.route("/admin")
@admin_required
def admin_dashboard():
    states = get_all_states()
    return render_template("admin/dashboard.html", states=states)


@admin_bp.route("/admin/states", methods=["POST"])
def update_states():
    selected_states = request.form.getlist("selected_states")
    selected_states = [int(state_id) for state_id in selected_states]
    update_selected_states(selected_states)
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/admin/ingest")
def admin_ingest():
    ingest_alerts()
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if validate_admin_login(username, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.admin_dashboard"))

        flash("Invalid Credentials")
    return render_template("admin/login.html")


@admin_bp.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin.admin_login"))
