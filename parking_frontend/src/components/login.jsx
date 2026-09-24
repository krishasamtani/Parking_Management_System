import React, { useState } from 'react';

export default function Login({ onLoginSuccess, onSwitchToRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        // Pass user info (like user_id) to parent component
        onLoginSuccess(data.user);
      } else {
        setMessage(data.message || 'Invalid credentials.');
      }
    } catch (err) {
      setMessage('Error connecting to server.');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: 'auto' }}>
      <h2>Login to Parking System</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label><br />
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label><br />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit" style={{ marginTop: '10px' }}>Login</button>
      </form>
      {message && <p>{message}</p>}
      <p style={{ marginTop: '15px' }}>
        Don't have an account? <button onClick={onSwitchToRegister}>Register here</button>
      </p>
    </div>
  );
}