from app import db
from sqlalchemy.sql import func

class reservation(db.Model):
    __tablename__ = 'reservation'
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.spot_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.lot_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    user_email = db.Column(db.String(100), db.ForeignKey('client.email', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    parking_time = db.Column(db.DateTime, nullable=False)
    leaving_time = db.Column(db.DateTime)
    vehicle_no = db.Column(db.String(20), nullable=False)
    total_cost = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # values: 'active', 'deleted'

    # This line is for reverse access ( backref = back reference to parent table )
    lot = db.relationship('parking_lot', backref='reservations')
    spot = db.relationship('parking_spot', backref='reservations')
    client = db.relationship('client', backref='reservations')
