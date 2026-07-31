import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Settings from './pages/Settings';
import StoragePage from './pages/Storage';
import VaultPage from './pages/Vault';
import WorkspacePage from './pages/Workspace';
import ProjectsPage from './pages/Projects';
import SnapshotsPage from './pages/Snapshots';
import BackupsPage from './pages/Backups';
import DocumentationPage from './pages/Documentation';
import DownloadsPage from './pages/Downloads';

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
                    <Route path="/storage" element={<StoragePage />} />
                    <Route path="/vault" element={<VaultPage />} />
                    <Route path="/workspaces" element={<WorkspacePage />} />
                    <Route path="/projects" element={<ProjectsPage />} />
                    <Route path="/snapshots" element={<SnapshotsPage />} />
                    <Route path="/backups" element={<BackupsPage />} />
                    <Route path="/documentation" element={<DocumentationPage />} />
                    <Route path="/downloads" element={<DownloadsPage />} />
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

