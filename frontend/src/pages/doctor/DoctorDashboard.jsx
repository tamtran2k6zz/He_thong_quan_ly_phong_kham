import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Stethoscope,
  Users,
  CheckCircle2,
  Clock,
  Sparkles,
  ClipboardList,
  ArrowRight,
  Activity,
  AlertTriangle,
  Play
} from 'lucide-react';
import { consultationService } from '../../services/consultationService';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import { formatDate, formatTime } from '../../utils/formatters';

const DoctorDashboard = () => {
  const { user } = useAuth();
  const [queue, setQueue] = useState([]);
  const [medicalRecords, setMedicalRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const loadData = async () => {
    setLoading(true);
    try {
      const [queueData, recordsData] = await Promise.all([
        consultationService.getQueue(),
        consultationService.getMedicalRecords({ limit: 20 }),
      ]);
      setQueue(queueData || []);
      setMedicalRecords(recordsData || []);
    } catch (err) {
      console.error('Failed to load doctor dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const waitingCount = queue.filter(q => q.status === 'CHECKED_IN').length;
  const inProgressCount = queue.filter(q => q.status === 'IN_PROGRESS').length;
  const completedTodayCount = medicalRecords.filter(r => r.status === 'COMPLETED').length;

  const nextPatient = queue.find(q => q.status === 'CHECKED_IN' || q.status === 'IN_PROGRESS');

  return (
    <div className="space-y-6">
      {/* Doctor Room Banner */}
      <div className="bg-gradient-to-r from-blue-700 via-sky-700 to-medical-800 p-6 rounded-3xl text-white shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-xs font-semibold mb-2">
            <Stethoscope className="w-3.5 h-3.5 text-sky-300" />
            Bàn khám Chuyên khoa • Phòng P101
          </div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
            Xin chào, {user?.full_name || 'Bác sĩ'}!
          </h1>
          <p className="text-xs text-sky-100 mt-1">
            Hôm nay bạn có <strong className="text-white underline">{queue.length} bệnh nhân</strong> trong danh sách chờ tiếp nhận.
          </p>
        </div>

        {nextPatient && (
          <button
            onClick={() => navigate(`/doctor/consultation?appointment_id=${nextPatient.appointment_id}&patient_id=${nextPatient.patient_id}`)}
            className="flex items-center gap-2 px-5 py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs rounded-2xl shadow-xl hover:shadow-2xl transition-all self-start sm:self-auto group"
          >
            <Play className="w-4 h-4 fill-current group-hover:scale-110 transition-transform" />
            Khám cho BN tiếp theo (#{nextPatient.queue_number || 1})
          </button>
        )}
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-3xl border border-emerald-200 bg-emerald-50/20 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-emerald-800">Đang chờ khám</span>
            <div className="p-2 bg-emerald-100 text-emerald-600 rounded-xl">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-emerald-900 mt-2">{waitingCount}</div>
          <div className="text-[11px] text-emerald-700 mt-1">Bệnh nhân đã tiếp đón</div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-indigo-200 bg-indigo-50/20 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-indigo-800">Đang thực hiện khám</span>
            <div className="p-2 bg-indigo-100 text-indigo-600 rounded-xl">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-indigo-900 mt-2">{inProgressCount}</div>
          <div className="text-[11px] text-indigo-700 mt-1">Hồ sơ đang mở</div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-2xs col-span-2 sm:col-span-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Đã hoàn tất ca khám</span>
            <div className="p-2 bg-slate-100 text-slate-600 rounded-xl">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-slate-900 mt-2">{completedTodayCount}</div>
          <div className="text-[11px] text-slate-400 mt-1">Đã kê đơn & hoàn tất hồ sơ</div>
        </div>
      </div>

      {/* Queue & Recent Records Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Waiting Room Queue (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-3xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 className="font-bold text-slate-900 text-base">Hàng chờ trước phòng khám</h2>
              <p className="text-xs text-slate-500">Thứ tự ưu tiên khám theo số tiếp nhận</p>
            </div>
            <Link
              to="/doctor/queue"
              className="text-xs font-bold text-medical-600 hover:text-medical-700 flex items-center gap-1"
            >
              Xem tất cả <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {queue.length === 0 ? (
              <div className="py-12 text-center text-slate-400 italic text-xs">
                {loading ? 'Đang tải hàng chờ...' : 'Hiện không có bệnh nhân nào trong hàng chờ khám'}
              </div>
            ) : (
              queue.slice(0, 5).map((item, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-2xl bg-slate-50 border border-slate-200 hover:border-medical-300 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-medical-600 text-white font-extrabold flex items-center justify-center font-mono text-base shadow-xs">
                      #{item.queue_number || idx + 1}
                    </div>
                    <div>
                      <div className="font-bold text-slate-900 text-sm">{item.patient_name}</div>
                      <div className="text-slate-500 text-[11px] flex items-center gap-2">
                        <span>Mã BN: <strong className="font-mono text-medical-700">{item.medical_code}</strong></span>
                        <span>• Giờ hẹn: {formatTime(item.start_time)}</span>
                      </div>
                      {item.reason && (
                        <div className="text-slate-600 text-[11px] italic mt-0.5">
                          Lý do: "{item.reason}"
                        </div>
                      )}
                    </div>
                  </div>

                  <button
                    onClick={() => navigate(`/doctor/consultation?appointment_id=${item.appointment_id}&patient_id=${item.patient_id}`)}
                    className="flex items-center gap-1.5 px-4 py-2 bg-medical-600 hover:bg-medical-700 text-white font-bold rounded-xl shadow-2xs transition-colors self-end sm:self-center text-xs"
                  >
                    <Stethoscope className="w-3.5 h-3.5" />
                    Vào khám ngay
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* AI Pre-visit Feature Highlight & Quick Actions (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-gradient-to-br from-sky-50 via-white to-indigo-50 border border-sky-200 rounded-3xl p-5 shadow-sm space-y-3">
            <div className="flex items-center gap-2.5 text-medical-800">
              <div className="p-2 bg-medical-600 text-white rounded-xl shadow-xs">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-sm">Trợ lý AI Bác sĩ (Clinical AI Assistant)</h3>
                <p className="text-[11px] text-slate-500">Hỗ trợ tự động hóa thủ tục lâm sàng</p>
              </div>
            </div>

            <div className="space-y-2 text-xs text-slate-600 pt-1 leading-relaxed">
              <div className="p-2.5 bg-white/90 rounded-xl border border-slate-200">
                <strong className="text-slate-900 block font-semibold">1. AI Pre-visit Briefing:</strong>
                Tóm tắt tiền sử dị ứng thuốc, bệnh lý mãn tính của bệnh nhân trước khi bước vào phòng.
              </div>
              <div className="p-2.5 bg-white/90 rounded-xl border border-slate-200">
                <strong className="text-slate-900 block font-semibold">2. AI Discharge Instructions:</strong>
                Tự động tạo hướng dẫn uống thuốc, dặn dò chế độ dinh dưỡng và lịch hẹn tái khám.
              </div>
            </div>

            <div className="text-[10px] text-amber-800 bg-amber-50 p-2.5 rounded-xl border border-amber-200">
              ⚠️ Mọi kết quả AI đều đi kèm Tuyên bố miễn trừ trách nhiệm y tế theo quy chuẩn y tế.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorDashboard;
