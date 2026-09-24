import React, { useEffect, useState } from 'react';

export default function ParkingDashboard({ user, onLogout }) {
  const [slots, setSlots] = useState([]);
  const [message, setMessage] = useState('');

  // Fetch slots from Flask backend
  const fetchSlots = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/slots');
      const data = await response.json();
      setSlots(data);
    } catch (err) {
      console.error('Error fetching slots:', err);
    }
  };

  useEffect(() => {
    fetchSlots();
  }, []);

  // Book a slot function
  const handleBookSlot = async (slotId) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id, slot_id: slotId }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        fetchSlots(); // Refresh slots after booking
      } else {
        setMessage(data.message);
      }
    } catch (err) {
      setMessage('Booking failed due to network error.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Welcome, {user.username} 👋</h2>
        <button onClick={onLogout}>Logout</button>
      </div>

      <h3>Available Parking Slots</h3>
      {message && <p style={{ color: 'blue' }}>{message}</p>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', marginTop: '20px' }}>
        {slots.map((slot) => (
          <div 
            key={slot.id} 
            style={{ 
              border: '1px solid #ccc', 
              padding: '15px', 
              borderRadius: '8px',
              backgroundColor: slot.is_available ? '#e6ffe6' : '#ffe6e6' 
            }}
          >
            <h4>Slot: {slot.slot_number}</h4>
            <p>Type: {slot.type}</p>
            <p>Status: {slot.is_available ? 'Available ✅' : 'Occupied ❌'}</p>
            
            {slot.is_available && (
              <button 
                onClick={() => handleBookSlot(slot.id)}
                style={{ backgroundColor: '#4CAF50', color: 'white', border: 'none', padding: '8px 12px', cursor: 'pointer' }}
              >
                Book Slot
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}