
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models import db, User
from extensions import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("reports.dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email", "").strip() or None
        password = request.form.get("password")
        role = request.form.get("role", "agent")
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "warning")
            return redirect(url_for("auth.register"))
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
