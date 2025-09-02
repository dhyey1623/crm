
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    db_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
