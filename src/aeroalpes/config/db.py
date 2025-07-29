from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = None


def init_db(app: Flask):
    """Initialize the SQLAlchemy instance for the given Flask app."""
    global db
    if db is None:
        db = SQLAlchemy(app)
    else:
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
    return db

