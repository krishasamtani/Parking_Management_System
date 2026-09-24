import React, { useState } from 'react';
import Login from './components/login';
import Register from './components/register';
import ParkingDashboard from './components/parkingdashboard';

export default function App() {
  const [currentView, setCurrentView] = useState('login'); // 'login', 'register', 'dashboard'
  const [user, setUser] = useState(null);

  return (
    <div>
      {currentView === 'login' && (
        <Login 
          onLoginSuccess={(userData) => {
            setUser(userData);
            setCurrentView('dashboard');
          }} 
          onSwitchToRegister={() => setCurrentView('register')} 
        />
      )}

      {currentView === 'register' && (
        <Register 
          onSwitchToLogin={() => setCurrentView('login')} 
        />
      )}

      {currentView === 'dashboard' && (
        <ParkingDashboard 
          user={user} 
          onLogout={() => {
            setUser(null);
            setCurrentView('login');
          }} 
        />
      )}
    </div>
  );
}