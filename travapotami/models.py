from .db import get_db

db = get_db()

class User(db.Model):
    # for database initialization testing
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=True,nullable=False)