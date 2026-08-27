import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Users,
  Calendar,
  UserCheck,
  Stethoscope,
  ClipboardList,
  FileSpreadsheet,
  Receipt,
  Pill,
  ShieldCheck,
  Bot,
  Layers,
  History,
  Building,
  ShieldAlert
} from 'lucide-react';

const Sidebar = ({ isOpen, onClose }) => {
  const { role } = useAuth();

  const getNavSections = () => {
    switch (role?.toLowerCase()) {
      case 'admin':
        return [
          {
            title: 'QUẢN TRỊ HỆ THỐNG',
            items: [
              { to: '/admin', label: 'Báo cáo & Thống kê', icon: LayoutDashboard, end: true },
              { to: '/admin/users', label: 'Quản lý tài khoản', icon: Users },
              { to: '/admin/doctors', label: 'Bác sĩ & Ca trực', icon: Stethoscope },
              { to: '/admin/medicines', label: 'Danh mục thuốc', icon: Pill },
            ],
          },
          {
            title: 'KIỂM TOÁN & AI GOVERNANCE',
            items: [
              { to: '/admin/audit-logs', label: 'Nhật ký truy cập (Audit)', icon: ShieldCheck },
              { to: '/admin/ai-logs', label: 'Nhật ký gọi AI (AI Logs)', icon: Bot },
            ],
          },
          {
            title: 'CHỨC NĂNG NGHIỆP VỤ',
            items: [
              { to: '/receptionist/patients', label: 'Tiếp nhận bệnh nhân', icon: UserCheck },
              { to: '/receptionist/appointments', label: 'Lịch khám bệnh', icon: Calendar },
              { to: '/doctor/queue', label: 'Hàng chờ khám bệnh', icon: ClipboardList },
              { to: '/accountant/invoices', label: 'Thu ngân & Viện phí', icon: Receipt },
            ]
          }
        ];

      case 'receptionist':
        return [
          {
            title: 'NGHIỆP VỤ TIẾP ĐÓN',
            items: [
              { to: '/receptionist', label: 'Tổng quan tiếp đón', icon: LayoutDashboard, end: true },
              { to: '/receptionist/patients', label: 'Hồ sơ & Đăng ký BN', icon: UserCheck },
              { to: '/receptionist/appointments', label: 'Lịch hẹn & Tiếp nhận', icon: Calendar },
            ],
          },
        ];

      case 'doctor':
        return [
          {
            title: 'PHÒNG KHÁM BỆNH',
            items: [
              { to: '/doctor', label: 'Bàn khám của tôi', icon: LayoutDashboard, end: true },
              { to: '/doctor/queue', label: 'Danh sách chờ khám', icon: ClipboardList },
              { to: '/doctor/consultation', label: 'Phiếu khám & Kê đơn', icon: Stethoscope },
            ],
          },
        ];

      case 'accountant':
        return [
          {
            title: 'VIỆN PHÍ & THU NGÂN',
            items: [
              { to: '/accountant', label: 'Báo cáo viện phí', icon: LayoutDashboard, end: true },
              { to: '/accountant/invoices', label: 'Thanh toán & Hóa đơn', icon: Receipt },
            ],
          },
        ];

      default:
        return [];
    }
  };

  const sections = getNavSections();

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/40 z-20 lg:hidden backdrop-blur-xs"
        />
      )}

      <aside
        className={`fixed top-[53px] bottom-0 left-0 z-20 w-64 bg-white border-r border-slate-200/90 overflow-y-auto transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-3.5 space-y-5">
          {sections.map((section, idx) => (
            <div key={idx} className="space-y-1">
              <div className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider font-mono">
                {section.title}
              </div>
              <nav className="mt-1.5 space-y-0.5">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      end={item.end}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all active:scale-[0.98] ${
                          isActive
                            ? 'bg-sky-50 text-sky-700 border border-sky-200/90 font-bold shadow-subtle'
                            : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                        }`
                      }
                    >
                      <Icon className="w-4 h-4 flex-shrink-0" />
                      <span>{item.label}</span>
                    </NavLink>
                  );
                })}
              </nav>
            </div>
          ))}
        </div>

        {/* Clinic Info Badge at Bottom */}
        <div className="p-3 m-3.5 bg-slate-50 border border-slate-200 rounded-xl text-[10px] text-slate-500 font-mono space-y-1">
          <div className="font-bold text-slate-700 flex items-center justify-between">
            <span>SDLC V1.0.0</span>
            <span className="text-emerald-600 flex items-center gap-1 font-semibold text-[9px]">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              RBAC OK
            </span>
          </div>
          <div className="text-slate-400 leading-tight">
            PII Redaction & Medical Guardrails Active
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
