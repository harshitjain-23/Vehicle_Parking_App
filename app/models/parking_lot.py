from app import db

class parking_lot(db.Model):
    lot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot')