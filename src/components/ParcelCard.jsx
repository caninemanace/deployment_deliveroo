import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import api from '../services/api';
import { Calendar, MapPin, Package, User, Weight } from 'lucide-react';
import { format } from 'date-fns';
import StatusBadge from './StatusBadge';

const VALID_STATUSES = [
  'pending',
  'picked_up',
  'in_transit',
  'delivered',
  'cancelled'
];

function ParcelCard({ parcel, onStatusUpdate }) {
  const { user } = useSelector(state => state.user);
  const [updating, setUpdating] = useState(false);
  const [newStatus, setNewStatus] = useState(parcel.status);

  const isCourier =
    user &&
    user.role === 'courier' &&
    parcel.courier &&
    parcel.courier.id === user.id;

  const handleStatusChange = async (e) => {
    const status = e.target.value;
    setNewStatus(status);
    setUpdating(true);
    try {
      await api.put(`/admin/parcels/${parcel.id}/status`, { status });
      if (onStatusUpdate) onStatusUpdate(parcel.id, status);
    } catch (err) {
      alert('Failed to update status');
    }
    setUpdating(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center space-x-2">
          <Package className="h-5 w-5 text-emerald-600" />
          <h3 className="text-lg font-semibold text-gray-800">
            {parcel.trackingNumber}
          </h3>
        </div>
        <StatusBadge status={parcel.status} />
      </div>

      <div className="space-y-3">
        <div className="flex items-center space-x-2 text-gray-600">
          <User className="h-4 w-4" />
          <span className="text-sm">
            {parcel.senderName} → {parcel.receiverName}
          </span>
        </div>

        <div className="flex items-center space-x-2 text-gray-600">
          <MapPin className="h-4 w-4" />
          <span className="text-sm">
            {parcel.pickupAddress} → {parcel.destinationAddress}
          </span>
        </div>

        {/* Assigned Courier Info */}
        {parcel.courier && (
          <div className="flex items-center space-x-2 text-gray-600 mt-2">
            <User className="h-4 w-4" />
            <span className="text-sm">
              Courier: {parcel.courier.name} ({parcel.courier.phone})
            </span>
          </div>
        )}

        {/* Status update for couriers */}
        {isCourier && (
          <div className="mt-2">
            <label className="text-sm mr-2">Update Status:</label>
            <select
              value={newStatus}
              onChange={handleStatusChange}
              disabled={updating}
              className="border rounded px-2 py-1"
            >
              {VALID_STATUSES.map(status => (
                <option key={status} value={status}>
                  {status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-gray-600">
            <Weight className="h-4 w-4" />
            <span className="text-sm">{parcel.weight} kg</span>
          </div>
          <div className="flex items-center space-x-2 text-gray-600">
            <Calendar className="h-4 w-4" />
            <span className="text-sm">
              {format(new Date(parcel.createdAt), 'MMM dd, yyyy')}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between pt-4">
          <span className="text-lg font-bold text-emerald-600">
            Ksh {parcel.price}
          </span>
          <Link
            to={`/parcel/${parcel.id}`}
            className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
}

export default ParcelCard;