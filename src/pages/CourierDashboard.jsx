import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import api from '../services/api';
import ParcelCard from '../components/ParcelCard';

function CourierDashboard() {
  const { user } = useSelector(state => state.user);
  const [parcels, setParcels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('all');
  const [error, setError] = useState(null);

  const fetchParcels = async () => {
    try {
      const token = localStorage.getItem('token');

      if (!token) {
        setError('No token found. Please log in.');
        setLoading(false);
        return;
      }

      const response = await api.get(`/couriers/parcels`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setParcels(response.data);
      setError(null);
    } catch (error) {
      if (error.response?.status === 403) {
        setError('Access denied. You must be logged in as a courier.');
      } else if (error.response?.status === 404) {
        setError('Courier profile not found. Please contact admin.');
      } else {
        setError('Failed to fetch parcels. Please try again later.');
      }
      setParcels([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchParcels();
    // eslint-disable-next-line
  }, []);

  const handleStatusUpdate = async () => {
    setLoading(true);
    await fetchParcels();
  };

  const filteredParcels = parcels.filter(parcel => {
    const nameMatch =
      parcel.senderName?.toLowerCase().includes(search.toLowerCase()) ||
      parcel.receiverName?.toLowerCase().includes(search.toLowerCase());
    const statusMatch =
      status === 'all' ? true : parcel.status === status;

    return nameMatch && statusMatch;
  });

  if (loading) return <div>Loading parcels...</div>;

  return (
    <div className="max-w-5xl mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Assigned Parcels</h1>

      {error && <div className="text-red-600 mb-4">{error}</div>}

      {!error && (
        <>
          <div className="flex flex-col md:flex-row md:items-center md:space-x-4 mb-6 space-y-2 md:space-y-0">
            <input
              type="text"
              placeholder="Search by sender or receiver name"
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="border px-3 py-2 rounded w-full md:w-1/2"
            />

            <select
              value={status}
              onChange={e => setStatus(e.target.value)}
              className="border px-3 py-2 rounded w-full md:w-1/4"
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="picked_up">Picked Up</option>
              <option value="in_transit">In Transit</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          {filteredParcels.length === 0 ? (
            <div className="text-gray-500">No parcels found.</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredParcels.map(parcel => (
                <ParcelCard
                  key={parcel.id}
                  parcel={parcel}
                  onStatusUpdate={handleStatusUpdate}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default CourierDashboard;

