from app import db

class parking_spot(db.Model):
    spot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.lot_id', ondelete='RESTRICT', onupdate='CASCADE'))
    status = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # True = exists, False = soft-deleted

    # This line is for reverse access ( backref = back reference to parent table )
    reservations = db.relationship('Reservation', backref='spot', lazy=True)
