import {BrowserRouter as Router, Routes, Route, Navigate, useNavigate} from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Vocabulary from './pages/Vocabulary';
import Datasets from './pages/Datasets';
import Progress from './pages/Progress';
import Settings from './pages/Settings';
import React, { useContext, useEffect } from 'react';
import { AuthProvider, useAuth } from './AuthContext'; // Import useAuth

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomeRedirect />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/vocabulary" element={<Vocabulary />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

function HomeRedirect() {
  const { isAuthenticated } = useAuth(); // Use useAuth to access isAuthenticated
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  return null; // Render nothing while redirecting
}

export default App;