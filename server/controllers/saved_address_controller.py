from flask import jsonify
from server.models import db, SavedAddress

class SavedAddressController:
    def get_addresses(self, user_id):
        addresses = SavedAddress.query.filter_by(user_id=user_id).all()
        return jsonify([{
            "id": a.id,
            "addressName": a.address_name,
            "address": a.address,
            "type": a.type,
            "latitude": a.latitude,
            "longitude": a.longitude
        } for a in addresses]), 200

    def create_address(self, user_id, data):
        try:
            new_address = SavedAddress(
                address_name=data.get("addressName"),
                address=data.get("address"),
                type=data.get("type", "home"),
                latitude=data.get("latitude"),
                longitude=data.get("longitude"),
                user_id=user_id
            )
            db.session.add(new_address)
            db.session.commit()
            return jsonify(new_address.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def update_address(self, user_id, address_id, data):
        address = SavedAddress.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return jsonify({"error": "Address not found."}), 404
        try:
            address.address_name = data.get("addressName", address.address_name)
            address.address = data.get("address", address.address)
            address.type = data.get("type", address.type)
            address.latitude = data.get("latitude", address.latitude)
            address.longitude = data.get("longitude", address.longitude)
            db.session.commit()
            return jsonify(address.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def delete_address(self, user_id, address_id):
        address = SavedAddress.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return jsonify({"error": "Address not found."}), 404
        db.session.delete(address)
        db.session.commit()
        return jsonify({"message": "Address deleted."}), 200

