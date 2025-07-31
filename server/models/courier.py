# courier.py
from server.models import db
from server.models.user import User

class Courier(db.Model):
    __tablename__ = 'couriers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    vehicle_type = db.Column(db.String(30), nullable=False)
    license_number = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='available')
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', back_populates='courier')
    parcels = db.relationship('Parcel', back_populates='courier', lazy=True)



