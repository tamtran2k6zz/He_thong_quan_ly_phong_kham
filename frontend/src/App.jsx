import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';

// Layout & Shared
import Layout from './components/Layout';

// Auth Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import BookAppointmentPage from './pages/BookAppointmentPage';
import UnauthorizedPage from './pages/UnauthorizedPage';

// Receptionist Pages
import ReceptionistDashboard from './pages/receptionist/ReceptionistDashboard';
import PatientRegistrationPage from './pages/receptionist/PatientRegistrationPage';
import AppointmentCalendarPage from './pages/receptionist/AppointmentCalendarPage';

// Doctor Pages
import DoctorDashboard from './pages/doctor/DoctorDashboard';
import PatientQueuePage from './pages/doctor/PatientQueuePage';
import ConsultationFormPage from './pages/doctor/ConsultationFormPage';

// Accountant Pages
import AccountantDashboard from './pages/accountant/AccountantDashboard';
import InvoicePaymentPage from './pages/accountant/InvoicePaymentPage';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagementPage from './pages/admin/UserManagementPage';
import DoctorShiftPage from './pages/admin/DoctorShiftPage';
import MedicineCatalogPage from './pages/admin/MedicineCatalogPage';
import AuditLogPage from './pages/admin/AuditLogPage';
import AILogPage from './pages/admin/AILogPage';

// Route Guard Component
const ProtectedRoute = ({ allowedRoles = [], children }) => {
  const { isAuthenticated, role, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-400 text-xs font-semibold">
        Đang khởi tạo hệ thống...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(role?.toLowerCase()) && role?.toLowerCase() !== 'admin') {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

// Root index redirector based on current user role
const RootRedirector = () => {
  const { isAuthenticated, role, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-400 text-xs font-semibold">
        Đang tải thông tin phiên...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  switch (role?.toLowerCase()) {
    case 'admin':
      return <Navigate to="/admin" replace />;
    case 'receptionist':
      return <Navigate to="/receptionist" replace />;
    case 'doctor':
      return <Navigate to="/doctor" replace />;
    case 'accountant':
      return <Navigate to="/accountant" replace />;
    default:
      return <Navigate to="/login" replace />;
  }
};

function App() {
  return (
    <BrowserRouter>
      <ToastProvider>
        <AuthProvider>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/book-appointment" element={<BookAppointmentPage />} />
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            <Route path="/" element={<RootRedirector />} />

            {/* Protected Routes inside Layout */}
            <Route
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              {/* Receptionist Subsystem */}
              <Route
                path="/receptionist"
                element={
                  <ProtectedRoute allowedRoles={['receptionist', 'admin']}>
                    <ReceptionistDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/receptionist/patients"
                element={
                  <ProtectedRoute allowedRoles={['receptionist', 'admin']}>
                    <PatientRegistrationPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/receptionist/appointments"
                element={
                  <ProtectedRoute allowedRoles={['receptionist', 'admin']}>
                    <AppointmentCalendarPage />
                  </ProtectedRoute>
                }
              />

              {/* Doctor Clinical Subsystem */}
              <Route
                path="/doctor"
                element={
                  <ProtectedRoute allowedRoles={['doctor', 'admin']}>
                    <DoctorDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/doctor/queue"
                element={
                  <ProtectedRoute allowedRoles={['doctor', 'admin']}>
                    <PatientQueuePage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/doctor/consultation"
                element={
                  <ProtectedRoute allowedRoles={['doctor', 'admin']}>
                    <ConsultationFormPage />
                  </ProtectedRoute>
                }
              />

              {/* Accountant Billing Subsystem */}
              <Route
                path="/accountant"
                element={
                  <ProtectedRoute allowedRoles={['accountant', 'admin']}>
                    <AccountantDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/accountant/invoices"
                element={
                  <ProtectedRoute allowedRoles={['accountant', 'admin']}>
                    <InvoicePaymentPage />
                  </ProtectedRoute>
                }
              />

              {/* Admin Governance Subsystem */}
              <Route
                path="/admin"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/users"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <UserManagementPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/doctors"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <DoctorShiftPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/medicines"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <MedicineCatalogPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/audit-logs"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <AuditLogPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/ai-logs"
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <AILogPage />
                  </ProtectedRoute>
                }
              />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </ToastProvider>
    </BrowserRouter>
  );
}

export default App;
