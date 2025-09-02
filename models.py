
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="agent")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    leads = db.relationship("Lead", backref="assignee", lazy=True)
    def is_admin(self): return self.role == "admin"

class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    property_type = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default="available")
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    leads = db.relationship("Lead", backref="property", lazy=True)

class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    leads = db.relationship("Lead", backref="client", lazy=True)

class Lead(db.Model):
    __tablename__ = "leads"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default="new")
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True)
