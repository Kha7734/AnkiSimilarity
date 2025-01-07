import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Vocabulary from './pages/Vocabulary';
import Datasets from './pages/Datasets';
import Progress from './pages/Progress';
import React from 'react';
import { AuthProvider } from './AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/vocabulary" element={<Vocabulary />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/progress" element={<Progress />} />
          {/*<Route path="/settings" element={<Settings />} />*/}
        </Routes>
      </Router>
    </AuthProvider>
  );
}


export default App;