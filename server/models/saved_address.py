from server.models import db
from sqlalchemy.orm import relationship
from datetime import datetime

class SavedAddress(db.Model):
    __tablename__ = 'saved_addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    address_name = db.Column(db.String(100), nullable=True)  # "Home", "Work", etc.
    address = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=True)  # home, work, favorite
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    user = db.relationship('User', back_populates='saved_addresses')

    def to_dict(self):
        return {
            'id': self.id,
            'addressName': self.address_name,
            'address': self.address,
            'type': self.type,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
