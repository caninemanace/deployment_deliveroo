from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import db, SavedAddress, User

saved_address_bp = Blueprint('saved_addresses', __name__)

@saved_address_bp.route('/saved-addresses', methods=['POST'])
@jwt_required()
def create_saved_address():
    user_id = get_jwt_identity()
    data = request.get_json()

    address_name = data.get('addressName')
    address = data.get('address')
    address_type = data.get('type', 'home')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not address:
        return jsonify({'error': 'Address is required'}), 400

    new_address = SavedAddress(
        user_id=user_id,
        address_name=address_name,
        address=address,
        type=address_type,
        latitude=latitude,
        longitude=longitude
    )

    db.session.add(new_address)
    db.session.commit()

    return jsonify(new_address.to_dict()), 201


@saved_address_bp.route('/saved-addresses', methods=['GET'])
@jwt_required()
def get_saved_addresses():
    user_id = get_jwt_identity()
    addresses = SavedAddress.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in addresses]), 200


@saved_address_bp.route('/saved-addresses/<int:id>', methods=['PUT'])
@jwt_required()
def update_saved_address(id):
    user_id = get_jwt_identity()
    saved = SavedAddress.query.filter_by(id=id, user_id=user_id).first()

    if not saved:
        return jsonify({'error': 'Saved address not found'}), 404

    data = request.get_json()

    saved.address_name = data.get('addressName', saved.address_name)
    saved.address = data.get('address', saved.address)
    saved.type = data.get('type', saved.type)
    saved.latitude = data.get('latitude', saved.latitude)
    saved.longitude = data.get('longitude', saved.longitude)

    db.session.commit()
    return jsonify(saved.to_dict()), 200


@saved_address_bp.route('/saved-addresses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_saved_address(id):
    user_id = get_jwt_identity()
    saved = SavedAddress.query.filter_by(id=id, user_id=user_id).first()

    if not saved:
        return jsonify({'error': 'Saved address not found'}), 404

    db.session.delete(saved)
    db.session.commit()
    return jsonify({'message': 'Saved address deleted'}), 200


