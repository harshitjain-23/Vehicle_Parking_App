from app import db

class superuser(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)