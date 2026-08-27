import React, { useState, useRef, useEffect } from 'react';
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
  Sparkles,
  CheckCircle2
} from 'lucide-react';
import { getRoleInfo } from '../utils/formatters';

const Navbar = ({ onToggleSidebar }) => {
  const { user, role, quickLogin, logout } = useAuth();
  const { toastSuccess, toastInfo } = useToast();
  const navigate = useNavigate();
  const [showRoleMenu, setShowRoleMenu] = useState(false);
  const dropdownRef = useRef(null);

  const roleInfo = getRoleInfo(role);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowRoleMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleRoleSwitch = async (roleKey) => {
    setShowRoleMenu(false);
    const result = await quickLogin(roleKey);
    if (result.success) {
      toastSuccess(`Đã chuyển sang vai trò: ${DEMO_ACCOUNTS[roleKey].name}`);
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
    toastInfo('Đã đăng xuất an toàn');
    navigate('/login');
  };

  return (
    <header className="bg-white/95 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-30 shadow-subtle">
      <div className="px-4 sm:px-6 py-2.5 flex items-center justify-between">
        {/* Left: Brand & Sidebar Toggle */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="p-1.5 rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden cursor-pointer active:scale-95 transition-all"
            aria-label="Toggle Menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-sky-600 to-teal-500 flex items-center justify-center text-white shadow-sm flex-shrink-0">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <div className="font-bold text-slate-900 text-sm font-display leading-tight flex items-center gap-2">
                SMART CLINIC ICTU
                <span className="hidden sm:inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200/80">
                  <Sparkles className="w-3 h-3 text-sky-500" /> AI Ready
                </span>
              </div>
              <p className="text-[10px] text-slate-500 hidden sm:block font-medium">
                Hệ thống Quản lý Y tế Đa khoa & Trợ lý AI Hành chính
              </p>
            </div>
          </div>
        </div>

        {/* Right: Role Switcher & User Profile */}
        <div className="flex items-center gap-2.5">
          {/* Quick Demo Switcher Dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setShowRoleMenu(!showRoleMenu)}
              className="flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-100/80 hover:bg-slate-200/80 text-slate-700 rounded-lg text-xs font-semibold border border-slate-200 transition-all active:scale-[0.98] cursor-pointer"
              title="Chuyển đổi vai trò demo"
            >
              <span className="hidden md:inline text-slate-500 font-normal">Vai trò:</span>
              <span className="font-bold text-sky-700 uppercase font-mono text-[11px]">{role}</span>
              <ChevronDown className={`w-3.5 h-3.5 text-slate-500 transition-transform ${showRoleMenu ? 'rotate-180' : ''}`} />
            </button>

            {showRoleMenu && (
              <div className="absolute right-0 mt-2 w-60 bg-white rounded-xl shadow-xl border border-slate-200/90 py-1.5 z-50 animate-slide-up">
                <div className="px-3 py-1.5 border-b border-slate-100 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                  Chuyển nhanh tài khoản demo
                </div>
                <div className="p-1 space-y-0.5">
                  <button
                    onClick={() => handleRoleSwitch('admin')}
                    className="w-full px-2.5 py-1.5 text-left text-xs rounded-lg hover:bg-purple-50 flex items-center gap-2.5 transition-colors cursor-pointer"
                  >
                    <div className="w-6 h-6 rounded-md bg-purple-100 text-purple-700 flex items-center justify-center flex-shrink-0">
                      <Shield className="w-3.5 h-3.5" />
                    </div>
                    <div className="truncate">
                      <div className="font-bold text-purple-950">Quản trị viên (Admin)</div>
                      <div className="text-[10px] font-mono text-slate-400">admin / admin123</div>
                    </div>
                  </button>

                  <button
                    onClick={() => handleRoleSwitch('receptionist')}
                    className="w-full px-2.5 py-1.5 text-left text-xs rounded-lg hover:bg-emerald-50 flex items-center gap-2.5 transition-colors cursor-pointer"
                  >
                    <div className="w-6 h-6 rounded-md bg-emerald-100 text-emerald-700 flex items-center justify-center flex-shrink-0">
                      <Users className="w-3.5 h-3.5" />
                    </div>
                    <div className="truncate">
                      <div className="font-bold text-emerald-950">Lễ tân tiếp đón</div>
                      <div className="text-[10px] font-mono text-slate-400">receptionist / rec123</div>
                    </div>
                  </button>

                  <button
                    onClick={() => handleRoleSwitch('doctor')}
                    className="w-full px-2.5 py-1.5 text-left text-xs rounded-lg hover:bg-sky-50 flex items-center gap-2.5 transition-colors cursor-pointer"
                  >
                    <div className="w-6 h-6 rounded-md bg-sky-100 text-sky-700 flex items-center justify-center flex-shrink-0">
                      <Stethoscope className="w-3.5 h-3.5" />
                    </div>
                    <div className="truncate">
                      <div className="font-bold text-sky-950">Bác sĩ khám (BS. Nam)</div>
                      <div className="text-[10px] font-mono text-slate-400">dr_nam / doc123</div>
                    </div>
                  </button>

                  <button
                    onClick={() => handleRoleSwitch('accountant')}
                    className="w-full px-2.5 py-1.5 text-left text-xs rounded-lg hover:bg-amber-50 flex items-center gap-2.5 transition-colors cursor-pointer"
                  >
                    <div className="w-6 h-6 rounded-md bg-amber-100 text-amber-700 flex items-center justify-center flex-shrink-0">
                      <CreditCard className="w-3.5 h-3.5" />
                    </div>
                    <div className="truncate">
                      <div className="font-bold text-amber-950">Kế toán / Thu ngân</div>
                      <div className="text-[10px] font-mono text-slate-400">accountant / acc123</div>
                    </div>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User Profile Badge */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="w-7 h-7 rounded-full bg-sky-100 text-sky-800 border border-sky-200 flex items-center justify-center font-bold text-xs">
              {user?.full_name?.charAt(0) || <User className="w-3.5 h-3.5" />}
            </div>
            <div className="hidden lg:block text-left">
              <div className="text-xs font-bold text-slate-900 leading-tight truncate max-w-[130px]">
                {user?.full_name || 'Người dùng'}
              </div>
              <span className={`inline-block px-1.5 py-0.2 rounded text-[9px] font-semibold border ${roleInfo.color}`}>
                {roleInfo.label}
              </span>
            </div>

            <button
              onClick={handleLogout}
              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors ml-1 cursor-pointer active:scale-95"
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
