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
  CheckCircle2,
  ShieldCheck,
  Building2
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
      toastSuccess(`Đăng nhập thành công: ${DEMO_ACCOUNTS[roleKey].name}`);
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
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 sm:p-6 relative overflow-hidden">
      {/* Subtle Ambient Glow Mesh */}
      <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-4xl w-full bg-white rounded-2xl shadow-2xl overflow-hidden grid grid-cols-1 md:grid-cols-12 border border-slate-200/80 relative z-10 animate-fade-in">
        {/* Left Side: Medical Trust Brand & AI Capability Card */}
        <div className="md:col-span-5 bg-gradient-to-b from-slate-900 via-slate-900 to-medical-950 p-8 text-white flex flex-col justify-between border-r border-slate-800">
          <div>
            {/* Header Badge */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-teal-400 text-white flex items-center justify-center shadow-md font-bold">
                <Activity className="w-5 h-5" />
              </div>
              <div>
                <h1 className="font-extrabold text-base font-display tracking-tight text-white flex items-center gap-1.5">
                  SMART CLINIC ICTU
                </h1>
                <p className="text-[11px] text-slate-400 font-medium">Hệ thống Quản lý Y tế Đa khoa</p>
              </div>
            </div>

            {/* AI Highlight Section */}
            <div className="mt-8 space-y-4 text-xs text-slate-300 leading-relaxed">
              <div className="p-4 bg-slate-800/80 rounded-xl border border-slate-700/60 backdrop-blur-sm space-y-1.5">
                <div className="font-bold text-sky-300 flex items-center gap-1.5 text-xs">
                  <Sparkles className="w-4 h-4 text-sky-400" />
                  Trợ lý AI Hành chính Tích hợp
                </div>
                <p className="text-[11px] text-slate-300 leading-normal">
                  Khử định danh dữ liệu y tế (PII), tóm tắt tiền sử bệnh án & sinh hướng dẫn sau khám theo chuẩn an toàn y tế.
                </p>
              </div>

              <div className="space-y-2.5 pt-2">
                <div className="flex items-center gap-2.5 text-[11px] text-slate-300 font-medium">
                  <ShieldCheck className="w-4 h-4 text-teal-400 flex-shrink-0" />
                  <span>Phân quyền 4 vai trò độc lập (RBAC)</span>
                </div>
                <div className="flex items-center gap-2.5 text-[11px] text-slate-300 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-teal-400 flex-shrink-0" />
                  <span>Thuật toán ngăn ngừa trùng lịch khám</span>
                </div>
                <div className="flex items-center gap-2.5 text-[11px] text-slate-300 font-medium">
                  <Building2 className="w-4 h-4 text-teal-400 flex-shrink-0" />
                  <span>Kê đơn, tính BHYT & VietQR tức thì</span>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-6 text-[10px] font-mono text-slate-400 border-t border-slate-800 flex items-center justify-between">
            <span>ICTU PROJECT 2026-2027</span>
            <span className="flex items-center gap-1 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              SYSTEM ONLINE
            </span>
          </div>
        </div>

        {/* Right Side: Login Form & 1-Click Demo Accounts */}
        <div className="md:col-span-7 p-8 sm:p-10 flex flex-col justify-center bg-white">
          <div className="mb-6">
            <h2 className="text-xl font-bold font-display text-slate-900 tracking-tight">
              Đăng nhập hệ thống
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Nhập tài khoản của bạn hoặc chọn nhanh 1 tài khoản demo bên dưới
            </p>
          </div>

          {/* Standard Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">
                Tên đăng nhập
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="admin, receptionist, dr_nam, accountant..."
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">
                Mật khẩu
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-b from-sky-500 to-sky-600 hover:from-sky-600 hover:to-sky-700 disabled:opacity-50 text-white rounded-xl font-bold text-xs shadow-sm shadow-sky-500/25 active:scale-[0.98] transition-all flex items-center justify-center gap-2 border border-sky-400/20 cursor-pointer"
            >
              {loading ? 'Đang xác thực...' : 'Đăng nhập'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* 1-Click Quick Login Demo Buttons */}
          <div className="mt-7 pt-5 border-t border-slate-100">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                ⚡ Đăng nhập nhanh 1-Click
              </span>
              <span className="text-[10px] font-mono text-slate-400">Demo Profiles</span>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => handleQuickLogin('admin')}
                className="flex items-center gap-2.5 p-2.5 rounded-xl border border-purple-200/80 bg-purple-50/50 hover:bg-purple-100/70 text-left transition-all active:scale-[0.98] cursor-pointer"
              >
                <div className="w-7 h-7 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center flex-shrink-0">
                  <Shield className="w-3.5 h-3.5" />
                </div>
                <div className="truncate">
                  <div className="text-xs font-bold text-purple-950">Quản trị viên</div>
                  <div className="text-[10px] font-mono text-purple-600">admin / admin123</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('receptionist')}
                className="flex items-center gap-2.5 p-2.5 rounded-xl border border-emerald-200/80 bg-emerald-50/50 hover:bg-emerald-100/70 text-left transition-all active:scale-[0.98] cursor-pointer"
              >
                <div className="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center flex-shrink-0">
                  <Users className="w-3.5 h-3.5" />
                </div>
                <div className="truncate">
                  <div className="text-xs font-bold text-emerald-950">Lễ tân tiếp đón</div>
                  <div className="text-[10px] font-mono text-emerald-600">rec / rec123</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('doctor')}
                className="flex items-center gap-2.5 p-2.5 rounded-xl border border-sky-200/80 bg-sky-50/50 hover:bg-sky-100/70 text-left transition-all active:scale-[0.98] cursor-pointer"
              >
                <div className="w-7 h-7 rounded-lg bg-sky-100 text-sky-700 flex items-center justify-center flex-shrink-0">
                  <Stethoscope className="w-3.5 h-3.5" />
                </div>
                <div className="truncate">
                  <div className="text-xs font-bold text-sky-950">Bác sĩ khám</div>
                  <div className="text-[10px] font-mono text-sky-600">dr_nam / doc123</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => handleQuickLogin('accountant')}
                className="flex items-center gap-2.5 p-2.5 rounded-xl border border-amber-200/80 bg-amber-50/50 hover:bg-amber-100/70 text-left transition-all active:scale-[0.98] cursor-pointer"
              >
                <div className="w-7 h-7 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center flex-shrink-0">
                  <CreditCard className="w-3.5 h-3.5" />
                </div>
                <div className="truncate">
                  <div className="text-xs font-bold text-amber-950">Thu ngân / Viện phí</div>
                  <div className="text-[10px] font-mono text-amber-600">acc / acc123</div>
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
