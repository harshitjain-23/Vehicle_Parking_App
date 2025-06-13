from app import db

class parking_lot(db.Model):
    lot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'deleted'

    # This line is for reverse access ( backref = back reference to parent table )
    spots = db.relationship('ParkingSpot', backref='lot', lazy=True)

    @property
    def occupied_spots(self):
        return sum(1 for spot in self.spots if spot.status == 'occupied' and spot.is_active)

    @property
    def available_spots(self):
        return sum(1 for spot in self.spots if spot.status != 'occupied' and spot.is_active)
