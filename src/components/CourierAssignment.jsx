import React, { useEffect, useState } from 'react';
import api from '../services/api';

function CourierAssignment({ parcel, onAssign }) {
  const [couriers, setCouriers] = useState([]);
  const [selectedCourier, setSelectedCourier] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [assigning, setAssigning] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCouriers = async () => {
      try {
        const res = await api.get('/couriers');
        setCouriers(res.data);
      } catch (err) {
        setCouriers([]);
      }
    };
    if (showModal) fetchCouriers();
  }, [showModal]);

  const handleAssign = async () => {
    if (!selectedCourier) {
      setError('Please select a courier.');
      return;
    }
    setAssigning(true);
    setError('');
    try {
      await api.put(`/admin/parcels/${parcel.id}/assign_courier`, {
        courier_id: selectedCourier,
      });
      setShowModal(false);
      setSelectedCourier('');
      if (onAssign) onAssign();
    } catch (err) {
      setError('Failed to assign courier.');
    }
    setAssigning(false);
  };

  return (
    <div>
      <button
        onClick={() => setShowModal(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Assign Courier
      </button>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">Assign Courier</h2>
            <select
              className="w-full border rounded px-3 py-2 mb-4"
              value={selectedCourier}
              onChange={e => setSelectedCourier(e.target.value)}
            >
              <option value="">Select a courier</option>
              {couriers.map(courier => (
                <option key={courier.id} value={courier.id}>
                  {courier.name} ({courier.phone})
                </option>
              ))}
            </select>
            {error && <div className="text-red-600 mb-2">{error}</div>}
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                disabled={assigning}
              >
                Cancel
              </button>
              <button
                onClick={handleAssign}
                className="px-4 py-2 bg-emerald-600 text-white rounded hover:bg-emerald-700 transition"
                disabled={assigning}
              >
                {assigning ? 'Assigning...' : 'Assign'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CourierAssignment;