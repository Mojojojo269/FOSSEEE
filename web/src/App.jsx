import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import UploadPage from './components/UploadPage';
import Dashboard from './components/Dashboard';
import HistoryPage from './components/HistoryPage';
import Navigation from './components/Navigation';
import './App.css';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated() ? children : <Navigate to="/" />;
};

const AppRoutes = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route 
        path="/" 
        element={isAuthenticated() ? <Navigate to="/upload" /> : <Login />} 
      />
      <Route
        path="/upload"
        element={
          <ProtectedRoute>
            <>
              <Navigation />
              <UploadPage />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <>
              <Navigation />
              <Dashboard />
            </>
          </ProtectedRoute>
        }
      />
      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <>
              <Navigation />
              <HistoryPage />
            </>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
