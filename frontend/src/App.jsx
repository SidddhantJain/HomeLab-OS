import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Settings from './pages/Settings';

function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('homelab_user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem('homelab_user');
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('homelab_token');
    localStorage.removeItem('homelab_user');
    setUser(null);
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0b0f19]">
      <Routes>
        <Route path="/login" element={<Login onLoginSuccess={(u) => setUser(u)} />} />
        <Route
          path="/*"
          element={
            <div className="min-h-screen flex flex-col">
              <Navbar user={user} onLogout={handleLogout} />
              <div className="flex flex-1">
                <Sidebar />
                <main className="flex-1 p-6 overflow-y-auto">
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/settings" element={<Settings />} />
                  </Routes>
                </main>
              </div>
            </div>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
