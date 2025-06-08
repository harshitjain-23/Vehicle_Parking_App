from app import db

class parking_spot(db.Model):
    spot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.lot_id', ondelete='RESTRICT', onupdate='CASCADE'))
    status = db.Column(db.String(20), nullable=False)

    reservations = db.relationship('Reservation', backref='spot')