
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from models import db, Property

properties_bp = Blueprint("properties", __name__)

@properties_bp.route("/")
@login_required
def list_properties():
    q = request.args.get("q", "").strip()
    query = Property.query
    if q:
        like = f"%{q}%"
        query = query.filter((Property.title.ilike(like)) | (Property.location.ilike(like)))
    properties = query.order_by(Property.created_at.desc()).all()
    return render_template("properties.html", properties=properties, q=q)

@properties_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_property():
    if request.method == "POST":
        p = Property(
            title=request.form.get("title"),
            property_type=request.form.get("property_type"),
            location=request.form.get("location"),
            price=request.form.get("price") or None,
            status=request.form.get("status", "available"),
            description=request.form.get("description")
        )
        db.session.add(p)
        db.session.commit()
        flash("Property created.", "success")
        return redirect(url_for("properties.list_properties"))
    return render_template("property_form.html", property=None)

@properties_bp.route("/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def edit_property(pid):
    p = Property.query.get_or_404(pid)
    if request.method == "POST":
        p.title = request.form.get("title")
        p.property_type = request.form.get("property_type")
        p.location = request.form.get("location")
        p.price = request.form.get("price") or None
        p.status = request.form.get("status")
        p.description = request.form.get("description")
        db.session.commit()
        flash("Property updated.", "success")
        return redirect(url_for("properties.list_properties"))
    return render_template("property_form.html", property=p)

@properties_bp.route("/<int:pid>/delete", methods=["POST"])
@login_required
def delete_property(pid):
    p = Property.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Property deleted.", "info")
    return redirect(url_for("properties.list_properties"))

@properties_bp.route("/export.csv")
@login_required
def export_properties():
    properties = Property.query.order_by(Property.created_at.desc()).all()
    def generate():
        header = "ID,Title,Type,Location,Price,Status,CreatedAt\n"
        yield header
        for p in properties:
            row = f"{p.id},{p.title or ''},{p.property_type or ''},{p.location or ''},{p.price or ''},{p.status or ''},{p.created_at}\n"
            yield row
    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=properties.csv"})
