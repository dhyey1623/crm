
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User
from extensions import bcrypt

users_bp = Blueprint("users", __name__)

def admin_required():
    return current_user.is_authenticated and current_user.is_admin()

@users_bp.route("/")
@login_required
def list_users():
    if not admin_required():
        flash("Admin only.", "danger")
        return redirect(url_for("reports.dashboard"))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users.html", users=users)

@users_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_user():
    if not admin_required():
        flash("Admin only.", "danger")
        return redirect(url_for("users.list_users"))
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email") or None
        role = request.form.get("role", "agent")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "warning")
            return redirect(url_for("users.new_user"))
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, role=role, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash("User created.", "success")
        return redirect(url_for("users.list_users"))
    return render_template("user_form.html")

@users_bp.route("/<int:uid>/delete", methods=["POST"])
@login_required
def delete_user(uid):
    if not admin_required():
        flash("Admin only.", "danger")
        return redirect(url_for("users.list_users"))
    u = User.query.get_or_404(uid)
    db.session.delete(u)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for("users.list_users"))
