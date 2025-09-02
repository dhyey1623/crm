
from flask import Flask, render_template
from config import Config
from models import db, User, Lead, Property, Client
from extensions import bcrypt, login_manager

from routes.auth import auth_bp
from routes.leads import leads_bp
from routes.properties import properties_bp
from routes.clients import clients_bp
from routes.reports import reports_bp
from routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(leads_bp, url_prefix="/leads")
    app.register_blueprint(properties_bp, url_prefix="/properties")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.route("/")
    def index():
        counts = {
            "leads": Lead.query.count(),
            "properties": Property.query.count(),
            "clients": Client.query.count()
        }
        return render_template("index.html", counts=counts)

    return app

app = create_app()
