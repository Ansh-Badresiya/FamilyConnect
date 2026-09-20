import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';

import Home from './pages/Home';
import DashboardLayout from './layouts/DashboardLayout';
import CitizenDashboard from './pages/CitizenDashboard';
import CitizenSchemes from './pages/CitizenSchemes';
import CitizenApplications from './pages/CitizenApplications';
import CitizenChangeRequests from './pages/CitizenChangeRequests';
import CitizenFamilyTransfers from './pages/CitizenFamilyTransfers';

const PrivateRoute = ({ children, role }: { children: React.ReactNode, role?: string }) => {
  const { user, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" />;
  if (role && user.role !== role) {
    return <Navigate to="/dashboard" />;
  }
  return children;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      
      <Route element={<PrivateRoute><DashboardLayout /></PrivateRoute>}>
        <Route path="/dashboard" element={<PrivateRoute role="CITIZEN"><CitizenDashboard /></PrivateRoute>} />
        <Route path="/schemes" element={<PrivateRoute role="CITIZEN"><CitizenSchemes /></PrivateRoute>} />
        <Route path="/applications" element={<PrivateRoute role="CITIZEN"><CitizenApplications /></PrivateRoute>} />
        <Route path="/change-requests" element={<PrivateRoute role="CITIZEN"><CitizenChangeRequests /></PrivateRoute>} />
        <Route path="/family-transfers" element={<PrivateRoute role="CITIZEN"><CitizenFamilyTransfers /></PrivateRoute>} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <div className="flex flex-col h-screen">
        <div className="bg-yellow-100 border-b border-yellow-200 text-yellow-800 text-center py-2 text-sm font-bold shadow-sm z-50">
          ⚠️ Hackathon Demo • Synthetic Government Data
        </div>
        <div className="flex-1 overflow-auto">
          <Router>
            <AppRoutes />
          </Router>
        </div>
      </div>
    </AuthProvider>
  );
};

export default App;
