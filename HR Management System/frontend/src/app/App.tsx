import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import { Login } from '../app/pages/Login';
import { SignUp } from '../app/pages/SignUp';

import { EmployeeDashboard } from '../app/pages/EmployeeDashboard';
import { EmployeeAttendance } from '../app/pages/EmployeeAttendance';

import { HRDashboard } from '../app/pages/HRDashboard';
import { HRAttendance } from '../app/pages/HRAttendance';

import { AdminDashboard } from '../app/pages/AdminDashboard';
import { ProtectedRoute } from '..//app/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute roles={['Employee']}>
              <EmployeeDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/employee-attendance"
          element={
            <ProtectedRoute roles={['Employee']}>
              <EmployeeAttendance />
            </ProtectedRoute>
          }
        />

        <Route
          path="/hr-dashboard"
          element={
            <ProtectedRoute roles={['HR']}>
              <HRDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/hr-attendance"
          element={
            <ProtectedRoute roles={['HR']}>
              <HRAttendance />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin-dashboard"
          element={
            <ProtectedRoute roles={['Admin']}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
