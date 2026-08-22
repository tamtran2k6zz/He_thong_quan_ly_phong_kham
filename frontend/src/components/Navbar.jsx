import React, { useState } from 'react';
import { useAuth, DEMO_ACCOUNTS } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { useNavigate } from 'react-router-dom';
import {
  Activity,
  LogOut,
  User,
  Shield,
  Stethoscope,
  Users,
  CreditCard,
  ChevronDown,
  Menu,
  Sparkles
} from 'lucide-react';
import { getRoleInfo } from '../utils/formatters';

const Navbar = ({ onToggleSidebar }) => {
  const { user, role, quickLogin, logout } = useAuth();
  const { toastSuccess, toastInfo } = useToast();
  const navigate = useNavigate();
  const [showRoleMenu, setShowRoleMenu] = useState(false);

  const roleInfo = getRoleInfo(role);

  const handleRoleSwitch = async (roleKey) => {
    setShowRoleMenu(false);
    const result = await quickLogin(roleKey);
    if (result.success) {
      toastSuccess(`Chuyển sang vai trò: ${DEMO_ACCOUNTS[roleKey].name}`);
      // Navigate to default view for role
      switch (roleKey) {
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
    }
  };

  const handleLogout = () => {
    logout();
    toastInfo('Đã đăng xuất khỏi hệ thống');
    navigate('/login');
  };

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
      <div className="px-4 sm:px-6 py-3 flex items-center justify-between">
        {/* Left: Brand / Sidebar Toggle */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden"
            aria-label="Toggle Menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-medical-600 to-sky-500 flex items-center justify-center text-white shadow-md">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="font-bold text-slate-900 text-sm sm:text-base leading-tight flex items-center gap-1.5">
                SMART CLINIC ICTU
                <span className="hidden sm:inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  <Sparkles className="w-3 h-3 text-emerald-600" /> AI Assistant
                </span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">
                Hệ thống Quản lý Y tế Đa khoa & Trợ lý AI Hành chính
              </p>
            </div>
          </div>
        </div>

        {/* Right: Quick Switcher & User Profile */}
        <div className="flex items-center gap-3">
          {/* Quick Role Switcher Dropdown (Crucial for live demo/examiner testing) */}
          <div className="relative">
            <button
              onClick={() => setShowRoleMenu(!showRoleMenu)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-200 transition-colors"
              title="Chuyển đổi vai trò demo"
            >
              <span className="hidden md:inline text-slate-500 font-normal">Chuyển vai trò:</span>
              <span className="font-bold text-medical-700 uppercase">{role}</span>
              <ChevronDown className="w-3.5 h-3.5 text-slate-500" />
            </button>

            {showRoleMenu && (
              <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-200 py-1 z-50 animate-in fade-in zoom-in-95 duration-150">
                <div className="px-3 py-2 border-b border-slate-100 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  Chuyển nhanh tài khoản demo
                </div>
                <button
                  onClick={() => handleRoleSwitch('admin')}
                  className="w-full px-3 py-2 text-left text-xs text-slate-700 hover:bg-purple-50 hover:text-purple-900 flex items-center gap-2.5 transition-colors"
                >
                  <Shield className="w-4 h-4 text-purple-600" />
                  <div>
                    <div className="font-semibold">Quản trị viên (Admin)</div>
                    <div className="text-[10px] text-slate-400">admin / admin123</div>
                  </div>
                </button>
                <button
                  onClick={() => handleRoleSwitch('receptionist')}
                  className="w-full px-3 py-2 text-left text-xs text-slate-700 hover:bg-emerald-50 hover:text-emerald-900 flex items-center gap-2.5 transition-colors"
                >
                  <Users className="w-4 h-4 text-emerald-600" />
                  <div>
                    <div className="font-semibold">Lễ tân tiếp đón</div>
                    <div className="text-[10px] text-slate-400">receptionist / rec123</div>
                  </div>
                </button>
                <button
                  onClick={() => handleRoleSwitch('doctor')}
                  className="w-full px-3 py-2 text-left text-xs text-slate-700 hover:bg-blue-50 hover:text-blue-900 flex items-center gap-2.5 transition-colors"
                >
                  <Stethoscope className="w-4 h-4 text-blue-600" />
                  <div>
                    <div className="font-semibold">Bác sĩ khám (BS. Nam)</div>
                    <div className="text-[10px] text-slate-400">dr_nam / doc123</div>
                  </div>
                </button>
                <button
                  onClick={() => handleRoleSwitch('accountant')}
                  className="w-full px-3 py-2 text-left text-xs text-slate-700 hover:bg-amber-50 hover:text-amber-900 flex items-center gap-2.5 transition-colors"
                >
                  <CreditCard className="w-4 h-4 text-amber-600" />
                  <div>
                    <div className="font-semibold">Kế toán / Thu ngân</div>
                    <div className="text-[10px] text-slate-400">accountant / acc123</div>
                  </div>
                </button>
              </div>
            )}
          </div>

          {/* User Profile Badge */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="w-8 h-8 rounded-full bg-medical-100 text-medical-700 border border-medical-200 flex items-center justify-center font-bold text-xs">
              {user?.full_name?.charAt(0) || <User className="w-4 h-4" />}
            </div>
            <div className="hidden lg:block text-left">
              <div className="text-xs font-bold text-slate-800 leading-tight truncate max-w-[140px]">
                {user?.full_name || 'Người dùng'}
              </div>
              <span className={`inline-block px-1.5 py-0.2 rounded text-[10px] font-semibold border ${roleInfo.color}`}>
                {roleInfo.label}
              </span>
            </div>

            <button
              onClick={handleLogout}
              className="p-2 text-slate-500 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors ml-1"
              title="Đăng xuất"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
