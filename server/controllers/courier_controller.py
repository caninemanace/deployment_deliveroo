from flask import jsonify, request
from server.models import db
from server.models.courier import Courier
from server.models.parcel import Parcel 
from server.models.user import User
from flask_jwt_extended import get_jwt_identity

class CourierController:
    def get_all_couriers(self):
        couriers = Courier.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'phone': c.phone,
            'vehicleType': c.vehicle_type,
            'licenseNumber': c.license_number,
            'status': c.status,
            'currentLat': c.current_lat,
            'currentLng': c.current_lng
        } for c in couriers])

    def create_courier(self, data):
        courier = Courier(
            name=data['name'],
            phone=data['phone'],
            vehicle_type=data['vehicleType'],
            license_number=data['licenseNumber'],
            status=data.get('status', 'available'),
            current_lat=data.get('currentLat'),
            current_lng=data.get('currentLng')
        )
        db.session.add(courier)
        db.session.commit()
        return jsonify({'message': 'Courier created', 'id': courier.id}), 201

    def update_courier(self, courier_id, data):
        courier = Courier.query.get_or_404(courier_id)
        courier.name = data.get('name', courier.name)
        courier.phone = data.get('phone', courier.phone)
        courier.vehicle_type = data.get('vehicleType', courier.vehicle_type)
        courier.license_number = data.get('licenseNumber', courier.license_number)
        courier.status = data.get('status', courier.status)
        courier.current_lat = data.get('currentLat', courier.current_lat)
        courier.current_lng = data.get('currentLng', courier.current_lng)
        db.session.commit()
        return jsonify({'message': 'Courier updated'})

    def delete_courier(self, courier_id):
        courier = Courier.query.get_or_404(courier_id)
        db.session.delete(courier)
        db.session.commit()
        return jsonify({'message': 'Courier deleted'})
    

    def get_all_parcels(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        # Ensure user exists and is a courier
        if not user or user.role != 'courier':
            return jsonify({'error': 'Access denied'}), 403

        # Get the courier instance linked to this user
        courier = Courier.query.filter_by(user_id=user.id).first()

        if not courier:
            return jsonify({'error': 'Courier profile not found for this user'}), 404

        # Get all parcels assigned to this courier
        parcels = Parcel.query.filter_by(courier_id=courier.id).all()
        return jsonify([parcel.to_dict() for parcel in parcels]), 200