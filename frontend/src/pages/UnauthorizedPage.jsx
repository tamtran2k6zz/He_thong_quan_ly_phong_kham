import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldAlert, ArrowLeft, Home } from 'lucide-react';

const UnauthorizedPage = () => {
  const navigate = useNavigate();
  const { role } = useAuth();

  const getRoleHome = () => {
    switch (role?.toLowerCase()) {
      case 'admin':
        return '/admin';
      case 'receptionist':
        return '/receptionist';
      case 'doctor':
        return '/doctor';
      case 'accountant':
        return '/accountant';
      default:
        return '/login';
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl p-8 shadow-xl border border-slate-200 text-center space-y-6">
        <div className="w-16 h-16 bg-rose-100 text-rose-600 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
          <ShieldAlert className="w-8 h-8" />
        </div>

        <div className="space-y-2">
          <h1 className="text-2xl font-bold text-slate-900">403 - Quyền truy cập bị từ chối</h1>
          <p className="text-xs text-slate-500 leading-relaxed">
            Bạn không có quyền truy cập vào phân hệ này. Cơ chế phân quyền RBAC yêu cầu vai trò tương ứng để bảo vệ tính bảo mật của dữ liệu y tế.
          </p>
        </div>

        <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600">
          Vai trò hiện tại của bạn: <strong className="uppercase text-medical-700">{role || 'Chưa xác định'}</strong>
        </div>

        <div className="flex gap-3 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl transition-colors"
          >
            <ArrowLeft className="w-4 h-4" /> Quay lại
          </button>
          <button
            onClick={() => navigate(getRoleHome())}
            className="flex items-center gap-1.5 px-4 py-2 bg-medical-600 hover:bg-medical-700 text-white text-xs font-semibold rounded-xl shadow transition-colors"
          >
            <Home className="w-4 h-4" /> Về trang chủ của tôi
          </button>
        </div>
      </div>
    </div>
  );
};

export default UnauthorizedPage;
