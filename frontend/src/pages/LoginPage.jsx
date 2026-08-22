import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, DEMO_ACCOUNTS } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import {
  Activity,
  Lock,
  User,
  Shield,
  Stethoscope,
  Users,
  CreditCard,
  ArrowRight,
  Sparkles,
  CheckCircle2
} from 'lucide-react';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, quickLogin } = useAuth();
  const { toastSuccess, toastError } = useToast();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      toastError('Vui lòng nhập tên đăng nhập và mật khẩu');
      return;
    }

    setLoading(true);
    const result = await login(username, password);
    setLoading(false);

    if (result.success) {
      toastSuccess(`Xin chào, ${result.user.full_name}!`);
      redirectToDashboard(result.user.role);
    } else {
      toastError(result.error || 'Đăng nhập không thành công');
    }
  };

  const handleQuickLogin = async (roleKey) => {
    setLoading(true);
    const result = await quickLogin(roleKey);
    setLoading(false);

    if (result.success) {
      toastSuccess(`Đăng nhập thành công với vai trò: ${DEMO_ACCOUNTS[roleKey].name}`);
      redirectToDashboard(result.user.role);
    } else {
      toastError(result.error || 'Đăng nhập thất bại');
    }
  };

  const redirectToDashboard = (role) => {
    switch (role?.toLowerCase()) {
      case 'admin':
        navigate('/admin');
        break;
      case 'receptionist':
        navigate('/receptionist');
        break;
      case 'doctor':
        navigate('/doctor');
        break;
      case 'accountant':
        navigate('/accountant');
        break;
      default:
        navigate('/');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-medical-950 to-slate-900 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white rounded-3xl shadow-2xl overflow-hidden grid grid-cols-1 md:grid-cols-12 border border-slate-700/30">
        {/* Left Side: Branding & AI Highlights */}
        <div className="md:col-span-5 bg-gradient-to-br from-medical-700 via-medical-800 to-sky-900 p-8 text-white flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-white text-medical-700 flex items-center justify-center shadow-lg font-bold">
                <Activity className="w-6 h-6" />
              </div>
              <div>
                <h1 className="font-extrabold text-lg tracking-tight leading-tight">
                  SMART CLINIC ICTU
                </h1>
                <p className="text-xs text-sky-200">Hệ thống Quản lý Y tế Đa khoa</p>
              </div>
            </div>

            <div className="mt-8 space-y-4 text-xs text-sky-100/90 leading-relaxed">
              <div className="p-3 bg-white/10 rounded-xl backdrop-blur-sm border border-white/10 space-y-1">
                <div className="font-semibold text-white flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-emerald-300" />
                  Trợ lý AI Hành chính
                </div>
                <p className="text-[11px] text-sky-200">
                  Tự động khử định danh dữ liệu y tế (PII), tóm tắt hồ sơ tiền sử & sinh hướng dẫn sau khám.
                </p>
              </div>

              <div className="space-y-2 pt-2">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>Phân quyền 4 vai trò độc lập (RBAC)</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>Thuật toán ngăn ngừa trùng lịch khám</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span>Kê đơn, tính BHYT & VietQR tức thì</span>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-8 text-[11px] text-sky-300/80 border-t border-white/10">
            Dự án Ứng dụng Trí tuệ Nhân tạo ICTU 2026 - 2027
          </div>
        </div>

        {/* Right Side: Login Form & 1-Click Demo Accounts */}
        <div className="md:col-span-7 p-8 sm:p-10 flex flex-col justify-center">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              Đăng nhập hệ thống
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Nhập tài khoản hoặc chọn 1 tài khoản demo bên dưới để bắt đầu
            </p>
          </div>

          {/* Standard Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Tên đăng nhập
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="admin, receptionist, dr_nam, accountant..."
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-medical-500 focus:border-transparent transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Mật khẩu
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-medical-500 focus:border-transparent transition-colors"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-medical-600 hover:bg-medical-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2"
            >
              {loading ? 'Đang xác thực...' : 'Đăng nhập'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* 1-Click Quick Login Demo Buttons */}
          <div className="mt-8 pt-6 border-t border-slate-200">
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-3">
              ⚡ Đăng nhập nhanh 1-Click (Tài khoản Demo)
            </div>
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleQuickLogin('admin')}
                className="flex items-center gap-2 p-2.5 rounded-xl border border-purple-200 bg-purple-50/70 hover:bg-purple-100 text-left transition-colors"
              >
                <Shield className="w-4 h-4 text-purple-600 flex-shrink-0" />
                <div className="truncate">
                  <div className="text-xs font-bold text-purple-900">Quản trị viên</div>
                  <div className="text-[10px] text-purple-700">admin / admin123</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('receptionist')}
                className="flex items-center gap-2 p-2.5 rounded-xl border border-emerald-200 bg-emerald-50/70 hover:bg-emerald-100 text-left transition-colors"
              >
                <Users className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <div className="truncate">
                  <div className="text-xs font-bold text-emerald-900">Lễ tân tiếp đón</div>
                  <div className="text-[10px] text-emerald-700">receptionist / rec123</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('doctor')}
                className="flex items-center gap-2 p-2.5 rounded-xl border border-blue-200 bg-blue-50/70 hover:bg-blue-100 text-left transition-colors"
              >
                <Stethoscope className="w-4 h-4 text-blue-600 flex-shrink-0" />
                <div className="truncate">
                  <div className="text-xs font-bold text-blue-900">Bác sĩ khám</div>
                  <div className="text-[10px] text-blue-700">dr_nam / doc123</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('accountant')}
                className="flex items-center gap-2 p-2.5 rounded-xl border border-amber-200 bg-amber-50/70 hover:bg-amber-100 text-left transition-colors"
              >
                <CreditCard className="w-4 h-4 text-amber-600 flex-shrink-0" />
                <div className="truncate">
                  <div className="text-xs font-bold text-amber-900">Kế toán / Thu ngân</div>
                  <div className="text-[10px] text-amber-700">accountant / acc123</div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
