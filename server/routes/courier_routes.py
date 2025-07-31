from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from server.controllers.courier_controller import CourierController

courier_bp = Blueprint('courier', __name__)
courier_controller = CourierController()

@courier_bp.route('', methods=['GET'])
@jwt_required()
@admin_required
def get_all_couriers():
    return courier_controller.get_all_couriers()

@courier_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def create_courier():
    data = request.get_json()
    return courier_controller.create_courier(data)

@courier_bp.route('/<int:courier_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_courier(courier_id):
    data = request.get_json()
    return courier_controller.update_courier(courier_id, data)

@courier_bp.route('/<int:courier_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_courier(courier_id):
    return courier_controller.delete_courier(courier_id)

@courier_bp.route('/parcels', methods=['GET'])
@jwt_required()
def get_all_parcels_for_couriers():
    return courier_controller.get_all_parcels()
