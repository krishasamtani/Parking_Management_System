import React, { useState } from 'react';

export default function Register({ onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage('Registration successful! Please login.');
      } else {
        setMessage(data.message || 'Registration failed.');
      }
    } catch (err) {
      setMessage('Error connecting to server.');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: 'auto' }}>
      <h2>Register for Parking</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>Username:</label><br />
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div>
          <label>Email:</label><br />
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label><br />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit" style={{ marginTop: '10px' }}>Register</button>
      </form>
      {message && <p>{message}</p>}
      <p style={{ marginTop: '15px' }}>
        Already have an account? <button onClick={onSwitchToLogin}>Login here</button>
      </p>
    </div>
  );
}