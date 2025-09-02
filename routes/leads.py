
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from models import db, Lead, User, Property, Client

leads_bp = Blueprint("leads", __name__)

@leads_bp.route("/")
@login_required
def list_leads():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    query = Lead.query
    if q:
        like = f"%{q}%"
        query = query.filter((Lead.name.ilike(like)) | (Lead.email.ilike(like)) | (Lead.phone.ilike(like)))
    if status:
        query = query.filter_by(status=status)
    leads = query.order_by(Lead.created_at.desc()).all()
    users = User.query.all()
    properties = Property.query.all()
    clients = Client.query.all()
    return render_template("leads.html", leads=leads, users=users, properties=properties, clients=clients, q=q, status=status)

@leads_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_lead():
    if request.method == "POST":
        lead = Lead(
            name=request.form.get("name"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            source=request.form.get("source"),
            status=request.form.get("status", "new"),
            notes=request.form.get("notes"),
            assigned_to=request.form.get("assigned_to") or None,
            property_id=request.form.get("property_id") or None,
            client_id=request.form.get("client_id") or None,
        )
        db.session.add(lead)
        db.session.commit()
        flash("Lead created.", "success")
        return redirect(url_for("leads.list_leads"))
    users = User.query.all()
    properties = Property.query.all()
    clients = Client.query.all()
    return render_template("lead_form.html", users=users, properties=properties, clients=clients, lead=None)

@leads_bp.route("/<int:lead_id>/edit", methods=["GET", "POST"])
@login_required
def edit_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    if request.method == "POST":
        lead.name = request.form.get("name")
        lead.email = request.form.get("email")
        lead.phone = request.form.get("phone")
        lead.source = request.form.get("source")
        lead.status = request.form.get("status")
        lead.notes = request.form.get("notes")
        lead.assigned_to = request.form.get("assigned_to") or None
        lead.property_id = request.form.get("property_id") or None
        lead.client_id = request.form.get("client_id") or None
        db.session.commit()
        flash("Lead updated.", "success")
        return redirect(url_for("leads.list_leads"))
    users = User.query.all()
    properties = Property.query.all()
    clients = Client.query.all()
    return render_template("lead_form.html", users=users, properties=properties, clients=clients, lead=lead)

@leads_bp.route("/<int:lead_id>/delete", methods=["POST"])
@login_required
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    flash("Lead deleted.", "info")
    return redirect(url_for("leads.list_leads"))

@leads_bp.route("/export.csv")
@login_required
def export_leads():
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    def generate():
        header = "ID,Name,Email,Phone,Source,Status,AssignedTo,PropertyID,ClientID,CreatedAt\n"
        yield header
        for l in leads:
            row = f"{l.id},{l.name or ''},{l.email or ''},{l.phone or ''},{l.source or ''},{l.status or ''},{l.assigned_to or ''},{l.property_id or ''},{l.client_id or ''},{l.created_at}\n"
            yield row
    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=leads.csv"})
