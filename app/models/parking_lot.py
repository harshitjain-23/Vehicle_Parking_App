from app import db

class parking_lot(db.Model):
    __tablename__ = 'parking_lot'
    lot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'deleted'

    # This line is for reverse access ( backref = back reference to parent table )
    spots = db.relationship('parking_spot', backref='lot', lazy=True)

    @property
    def total_no_spots(self):
        return len([spot for spot in self.spots if spot.is_active])

    @property
    def occupied_spots(self):
        return len([spot for spot in self.spots if spot.is_active and spot.status == 'occupied'])

