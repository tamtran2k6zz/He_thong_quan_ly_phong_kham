import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ClipboardList,
  Users,
  Clock,
  Stethoscope,
  Search,
  Filter,
  ArrowRight,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { consultationService } from '../../services/consultationService';
import { useToast } from '../../context/ToastContext';
import { formatTime, formatDate } from '../../utils/formatters';

const PatientQueuePage = () => {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const { toastSuccess, toastError } = useToast();
  const navigate = useNavigate();

  const loadQueue = async () => {
    setLoading(true);
    try {
      const data = await consultationService.getQueue();
      setQueue(data || []);
    } catch (err) {
      console.error('Failed to load consultation queue:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQueue();
  }, []);

  const filteredQueue = queue.filter((item) => {
    if (!searchTerm) return true;
    const q = searchTerm.toLowerCase();
    return (
      item.patient_name?.toLowerCase().includes(q) ||
      item.medical_code?.toLowerCase().includes(q) ||
      item.doctor_name?.toLowerCase().includes(q) ||
      item.appointment_code?.toLowerCase().includes(q)
    );
  });

  const handleStartExam = (item) => {
    navigate(`/doctor/consultation?appointment_id=${item.appointment_id}&patient_id=${item.patient_id}`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <ClipboardList className="w-6 h-6 text-medical-600" />
            Hàng chờ tiếp nhận khám bệnh (Waiting Queue)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Danh sách bệnh nhân đã hoàn tất thủ tục tiếp đón tại quầy Lễ tân
          </p>
        </div>

        <button
          onClick={loadQueue}
          disabled={loading}
          className="flex items-center gap-1.5 px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-bold shadow-2xs transition-colors self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Làm mới hàng chờ
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Tìm kiếm theo Tên bệnh nhân, Mã BN, Bác sĩ phụ trách..."
          className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-medical-500 shadow-2xs"
        />
      </div>

      {/* Queue Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Số thứ tự (STT)</th>
                <th className="py-3.5 px-4">Bệnh nhân / Mã BN</th>
                <th className="py-3.5 px-4">Giờ tiếp đón</th>
                <th className="py-3.5 px-4">Bác sĩ & Phòng khám</th>
                <th className="py-3.5 px-4">Lý do khám / Triệu chứng</th>
                <th className="py-3.5 px-4">Trạng thái</th>
                <th className="py-3.5 px-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-400 italic">
                    Đang tải danh sách hàng chờ khám...
                  </td>
                </tr>
              ) : filteredQueue.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-400 italic">
                    Không có bệnh nhân nào trong hàng chờ lúc này
                  </td>
                </tr>
              ) : (
                filteredQueue.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-4 px-4">
                      <div className="w-9 h-9 rounded-xl bg-medical-600 text-white font-extrabold flex items-center justify-center font-mono text-sm shadow-xs">
                        #{item.queue_number || idx + 1}
                      </div>
                    </td>

                    <td className="py-4 px-4">
                      <div className="font-bold text-slate-900 text-sm">{item.patient_name}</div>
                      <div className="font-mono text-[11px] text-medical-700 font-semibold">{item.medical_code}</div>
                    </td>

                    <td className="py-4 px-4 text-slate-600 font-medium">
                      <div className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {formatTime(item.start_time)}
                      </div>
                      <div className="text-[10px] text-slate-400">{formatDate(item.appointment_date)}</div>
                    </td>

                    <td className="py-4 px-4">
                      <div className="font-semibold text-slate-800">{item.doctor_name}</div>
                      <div className="text-medical-700 text-[11px] font-semibold">Phòng: {item.clinic_room}</div>
                    </td>

                    <td className="py-4 px-4 max-w-xs text-slate-600 truncate">
                      {item.reason || 'Khám lâm sàng tổng quát'}
                    </td>

                    <td className="py-4 px-4">
                      <span className={`inline-flex px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                        item.status === 'IN_PROGRESS'
                          ? 'bg-indigo-100 text-indigo-800 border-indigo-200 animate-pulse'
                          : 'bg-emerald-100 text-emerald-800 border-emerald-200'
                      }`}>
                        {item.status === 'IN_PROGRESS' ? 'ĐANG KHÁM' : 'CHỜ TIẾP NHẬN'}
                      </span>
                    </td>

                    <td className="py-4 px-4 text-right">
                      <button
                        onClick={() => handleStartExam(item)}
                        className="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-medical-600 hover:bg-medical-700 text-white rounded-xl font-bold text-xs shadow-2xs transition-colors"
                      >
                        <Stethoscope className="w-3.5 h-3.5" />
                        Bắt đầu khám
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default PatientQueuePage;
