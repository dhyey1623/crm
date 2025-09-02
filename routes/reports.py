
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models import Lead, Property, Client, User
from sqlalchemy import func

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/dashboard")
@login_required
def dashboard():
    counts = {
        "leads": Lead.query.count(),
        "properties": Property.query.count(),
        "clients": Client.query.count(),
        "agents": User.query.filter_by(role="agent").count()
    }
    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()
    return render_template("dashboard.html", counts=counts, recent_leads=recent_leads)

@reports_bp.route("/data/leads_by_status")
@login_required
def leads_by_status():
    data = (Lead.query.with_entities(Lead.status, func.count(Lead.id))
            .group_by(Lead.status).all())
    labels = [d[0] for d in data]
    values = [int(d[1]) for d in data]
    return jsonify({"labels": labels, "values": values})

@reports_bp.route("/data/leads_by_agent")
@login_required
def leads_by_agent():
    data = (Lead.query.with_entities(User.username, func.count(Lead.id))
            .join(User, User.id == Lead.assigned_to)
            .group_by(User.username).all())
    labels = [d[0] for d in data]
    values = [int(d[1]) for d in data]
    return jsonify({"labels": labels, "values": values})
