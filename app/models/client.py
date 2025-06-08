from app import db

class client(db.Model):
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)