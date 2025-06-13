from app import db

class parking_spot(db.Model):
    __tablename__ = 'parking_spot'
    spot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.lot_id', ondelete='RESTRICT', onupdate='CASCADE'))
    status = db.Column(db.String(20), nullable=False) # status = 'occupied' or 'available'
    is_active = db.Column(db.Boolean, default=True)  # True = exists, False = deleted
