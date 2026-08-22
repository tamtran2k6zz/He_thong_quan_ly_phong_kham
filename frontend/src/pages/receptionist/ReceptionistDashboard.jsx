import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Users,
  Calendar,
  Clock,
  CheckCircle2,
  AlertCircle,
  UserPlus,
  ArrowRight,
  Search,
  Check,
  X,
  Stethoscope,
  Activity,
  Bot
} from 'lucide-react';
import { appointmentService } from '../../services/appointmentService';
import { consultationService } from '../../services/consultationService';
import { useToast } from '../../context/ToastContext';
import { formatDate, formatTime, getAppointmentStatusInfo } from '../../utils/formatters';

const ReceptionistDashboard = () => {
  const [appointments, setAppointments] = useState([]);
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const { toastSuccess, toastError } = useToast();
  const navigate = useNavigate();

  const loadData = async () => {
    setLoading(true);
    try {
      const todayStr = new Date().toISOString().split('T')[0];
      const [apptsData, queueData] = await Promise.all([
        appointmentService.getAppointments({ limit: 100 }),
        consultationService.getQueue()
      ]);
      setAppointments(apptsData || []);
      setQueue(queueData || []);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCheckIn = async (appointmentId, code) => {
    try {
      await appointmentService.checkInAppointment(appointmentId);
      toastSuccess(`Đã tiếp đón bệnh nhân (Lịch hẹn: ${code}) vào hàng chờ khám!`);
      loadData();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Tiếp đón thất bại');
    }
  };

  const handleCancel = async (appointmentId, code) => {
    if (!window.confirm(`Bạn có chắc chắn muốn hủy lịch hẹn ${code}?`)) return;
    try {
      await appointmentService.cancelAppointment(appointmentId);
      toastSuccess(`Đã hủy lịch hẹn ${code}`);
      loadData();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Hủy lịch thất bại');
    }
  };

  // Metrics
  const totalToday = appointments.length;
  const checkedInCount = appointments.filter(a => a.status === 'CHECKED_IN').length;
  const inProgressCount = appointments.filter(a => a.status === 'IN_PROGRESS').length;
  const completedCount = appointments.filter(a => a.status === 'COMPLETED').length;

  const filteredAppointments = appointments.filter(a => {
    if (!searchTerm) return true;
    const q = searchTerm.toLowerCase();
    return (
      a.appointment_code?.toLowerCase().includes(q) ||
      a.patient?.full_name?.toLowerCase().includes(q) ||
      a.patient?.phone?.includes(q) ||
      a.doctor?.user?.full_name?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-gradient-to-r from-medical-700 to-sky-700 p-6 rounded-3xl text-white shadow-lg">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
            Bàn tiếp đón & Điều phối Lễ tân
          </h1>
          <p className="text-xs text-sky-100 mt-1">
            Tiếp đón bệnh nhân, kiểm tra danh sách lịch hẹn và điều phối hàng chờ khám
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <Link
            to="/receptionist/patients"
            className="flex items-center gap-1.5 px-4 py-2.5 bg-white text-medical-800 hover:bg-sky-50 text-xs font-bold rounded-xl shadow-md transition-all"
          >
            <UserPlus className="w-4 h-4 text-medical-600" />
            Đăng ký bệnh nhân mới
          </Link>
          <Link
            to="/receptionist/appointments"
            className="flex items-center gap-1.5 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold rounded-xl shadow-md transition-all"
          >
            <Calendar className="w-4 h-4" />
            Đặt lịch khám ngay
          </Link>
        </div>
      </div>

      {/* KPI Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Tổng lịch hẹn</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
              <Calendar className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-2">{totalToday}</div>
          <div className="text-[11px] text-slate-400 mt-1">Lịch khám ghi nhận</div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-2xl border border-emerald-200 bg-emerald-50/30 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-emerald-800">Đã tiếp đón (Chờ khám)</span>
            <div className="p-2 bg-emerald-100 text-emerald-600 rounded-xl">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-emerald-900 mt-2">{checkedInCount}</div>
          <div className="text-[11px] text-emerald-700 mt-1">Đang chờ trước phòng khám</div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-2xl border border-indigo-200 bg-indigo-50/30 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-indigo-800">Đang khám</span>
            <div className="p-2 bg-indigo-100 text-indigo-600 rounded-xl">
              <Stethoscope className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-indigo-900 mt-2">{inProgressCount}</div>
          <div className="text-[11px] text-indigo-700 mt-1">Bác sĩ đang thực hiện khám</div>
        </div>

        <div className="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Đã hoàn tất</span>
            <div className="p-2 bg-slate-100 text-slate-600 rounded-xl">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-2">{completedCount}</div>
          <div className="text-[11px] text-slate-400 mt-1">Đã có kết luận & đơn thuốc</div>
        </div>
      </div>

      {/* Main Grid: Today's Appointments & Live Queue */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Appointments Table (8 cols) */}
        <div className="lg:col-span-8 bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="font-bold text-slate-900 text-base">Danh sách lịch hẹn hôm nay</h2>
              <p className="text-xs text-slate-500">Bấm "Tiếp đón" để chuyển bệnh nhân vào phòng chờ của Bác sĩ</p>
            </div>

            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Tìm mã LH, bệnh nhân, SĐT..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-medical-500"
              />
            </div>
          </div>

          <div className="overflow-x-auto flex-1">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
                <tr>
                  <th className="py-3 px-4">Mã LH / Giờ</th>
                  <th className="py-3 px-4">Bệnh nhân</th>
                  <th className="py-3 px-4">Bác sĩ & Phòng</th>
                  <th className="py-3 px-4">Trạng thái</th>
                  <th className="py-3 px-4 text-right">Thao tác</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredAppointments.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="py-8 text-center text-slate-400 italic">
                      {loading ? 'Đang tải dữ liệu lịch hẹn...' : 'Không tìm thấy lịch hẹn phù hợp'}
                    </td>
                  </tr>
                ) : (
                  filteredAppointments.map((appt) => {
                    const statusInfo = getAppointmentStatusInfo(appt.status);
                    const patientName = appt.patient?.full_name || 'Bệnh nhân';
                    const docName = appt.doctor?.user?.full_name || 'Bác sĩ';
                    const room = appt.clinic?.room_number || 'P101';

                    return (
                      <tr key={appt.id} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3 px-4">
                          <div className="font-bold text-slate-900 font-mono">{appt.appointment_code}</div>
                          <div className="text-slate-500 text-[11px] flex items-center gap-1">
                            <Clock className="w-3 h-3 text-slate-400" />
                            {formatTime(appt.start_time)} - {formatDate(appt.appointment_date)}
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <div className="font-semibold text-slate-800">{patientName}</div>
                          <div className="text-slate-500 text-[11px]">
                            {appt.patient?.phone || 'Chưa có SĐT'} | Mã: {appt.patient?.medical_code || '---'}
                          </div>
                        </td>

                        <td className="py-3 px-4">
                          <div className="font-medium text-slate-800">{docName}</div>
                          <div className="text-medical-700 font-semibold text-[11px]">Phòng: {room}</div>
                        </td>

                        <td className="py-3 px-4">
                          <span className={`inline-flex px-2 py-0.5 rounded-full text-[10px] font-bold border ${statusInfo.color}`}>
                            {statusInfo.label}
                          </span>
                        </td>

                        <td className="py-3 px-4 text-right">
                          <div className="flex items-center justify-end gap-1.5">
                            {appt.status === 'CONFIRMED' || appt.status === 'PENDING' ? (
                              <button
                                onClick={() => handleCheckIn(appt.id, appt.appointment_code)}
                                className="flex items-center gap-1 px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold text-[11px] shadow-2xs transition-colors"
                                title="Tiếp đón bệnh nhân"
                              >
                                <Check className="w-3.5 h-3.5" />
                                Tiếp đón
                              </button>
                            ) : null}

                            {appt.status !== 'COMPLETED' && appt.status !== 'CANCELLED' && (
                              <button
                                onClick={() => handleCancel(appt.id, appt.appointment_code)}
                                className="p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                                title="Hủy lịch hẹn"
                              >
                                <X className="w-4 h-4" />
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Live Queue Overview (4 cols) */}
        <div className="lg:col-span-4 bg-white rounded-3xl border border-slate-200 shadow-sm p-5 flex flex-col space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-600" />
              <h3 className="font-bold text-slate-900 text-sm">Hàng chờ khám trực tiếp</h3>
            </div>
            <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-[10px] font-bold rounded-full">
              {queue.length} người chờ
            </span>
          </div>

          <div className="space-y-2.5 overflow-y-auto max-h-[480px]">
            {queue.length === 0 ? (
              <div className="text-center py-8 text-slate-400 text-xs italic">
                Hiện không có bệnh nhân nào trong hàng chờ
              </div>
            ) : (
              queue.map((item, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-2xl bg-slate-50 border border-slate-200 hover:border-emerald-300 transition-all flex items-center justify-between gap-2 text-xs"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white font-extrabold flex items-center justify-center font-mono text-sm shadow-xs">
                      #{item.queue_number || idx + 1}
                    </div>
                    <div>
                      <div className="font-bold text-slate-900">{item.patient_name}</div>
                      <div className="text-[11px] text-slate-500">
                        BS: {item.doctor_name} | {item.clinic_room}
                      </div>
                    </div>
                  </div>

                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-200 uppercase">
                    {item.status === 'IN_PROGRESS' ? 'Đang khám' : 'Chờ gọi'}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReceptionistDashboard;
