# parcel.py
from datetime import datetime
from server.models import db

class Parcel(db.Model):
    __tablename__ = 'parcels'

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    pickup_address = db.Column(db.Text, nullable=False)
    destination_address = db.Column(db.Text, nullable=False)
    pickup_lat = db.Column(db.Float, nullable=False)
    pickup_lng = db.Column(db.Float, nullable=False)
    destination_lat = db.Column(db.Float, nullable=False)
    destination_lng = db.Column(db.Float, nullable=False)
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    courier_id = db.Column(db.Integer, db.ForeignKey('couriers.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    courier = db.relationship('Courier', back_populates='parcels')
    owner = db.relationship('User', back_populates='parcels')
    locations = db.relationship('Location', backref='parcel', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'trackingNumber': self.tracking_number,
            'senderName': self.sender_name,
            'receiverName': self.receiver_name,
            'pickupAddress': self.pickup_address,
            'destinationAddress': self.destination_address,
            'pickupCoords': {'lat': self.pickup_lat, 'lng': self.pickup_lng},
            'destinationCoords': {'lat': self.destination_lat, 'lng': self.destination_lng},
            'currentLocation': {'lat': self.current_lat, 'lng': self.current_lng} if self.current_lat else None,
            'weight': self.weight,
            'price': self.price,
            'status': self.status,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'userId': self.user_id,
            'timeline': [location.to_dict() for location in self.locations],
            'canUpdate': self.status == 'pending',
            'courier': {
                'id': self.courier.id,
                'name': self.courier.name,
                'phone': self.courier.phone,
                'vehicleType': self.courier.vehicle_type,
                'licenseNumber': self.courier.license_number,
                'status': self.courier.status
            } if self.courier else None,
        }
