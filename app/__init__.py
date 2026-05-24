import os

from dotenv import load_dotenv
from flask import Flask

from app.services.init_db import initialize_database


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    initialize_database()

    from app.routes.admin_routes import admin_bp
    from app.routes.public_routes import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    return app
