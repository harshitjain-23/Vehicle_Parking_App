from app import db

class reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.spot_id', ondelete='RESTRICT', onupdate='CASCADE'))
    user_email = db.Column(db.String(100), db.ForeignKey('user.email', ondelete='RESTRICT', onupdate='CASCADE'))
    parking_time = db.Column(db.String(100), nullable=False)
    leaving_time = db.Column(db.String(100))
