
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from models import db, Client

clients_bp = Blueprint("clients", __name__)

@clients_bp.route("/")
@login_required
def list_clients():
    q = request.args.get("q", "").strip()
    query = Client.query
    if q:
        like = f"%{q}%"
        query = query.filter((Client.name.ilike(like)) | (Client.email.ilike(like)) | (Client.phone.ilike(like)))
    clients = query.order_by(Client.created_at.desc()).all()
    return render_template("clients.html", clients=clients, q=q)

@clients_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_client():
    if request.method == "POST":
        c = Client(
            name=request.form.get("name"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            address=request.form.get("address"),
            notes=request.form.get("notes")
        )
        db.session.add(c)
        db.session.commit()
        flash("Client added.", "success")
        return redirect(url_for("clients.list_clients"))
    return render_template("client_form.html", client=None)

@clients_bp.route("/<int:cid>/edit", methods=["GET", "POST"])
@login_required
def edit_client(cid):
    c = Client.query.get_or_404(cid)
    if request.method == "POST":
        c.name = request.form.get("name")
        c.email = request.form.get("email")
        c.phone = request.form.get("phone")
        c.address = request.form.get("address")
        c.notes = request.form.get("notes")
        db.session.commit()
        flash("Client updated.", "success")
        return redirect(url_for("clients.list_clients"))
    return render_template("client_form.html", client=c)

@clients_bp.route("/<int:cid>/delete", methods=["POST"])
@login_required
def delete_client(cid):
    c = Client.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    flash("Client deleted.", "info")
    return redirect(url_for("clients.list_clients"))

@clients_bp.route("/export.csv")
@login_required
def export_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    def generate():
        header = "ID,Name,Email,Phone,Address,CreatedAt\n"
        yield header
        for c in clients:
            row = f"{c.id},{c.name or ''},{c.email or ''},{c.phone or ''},{c.address or ''},{c.created_at}\n"
            yield row
    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=clients.csv"})
