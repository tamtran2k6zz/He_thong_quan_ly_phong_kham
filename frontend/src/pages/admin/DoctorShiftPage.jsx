import React, { useState, useEffect } from 'react';
import {
  Stethoscope,
  Building,
  Calendar,
  Clock,
  Plus,
  Search,
  UserCheck,
  CheckCircle2,
  X
} from 'lucide-react';
import { clinicService } from '../../services/clinicService';
import { useToast } from '../../context/ToastContext';
import { formatDate, formatTime } from '../../utils/formatters';

const DoctorShiftPage = () => {
  const [doctors, setDoctors] = useState([]);
  const [specialties, setSpecialties] = useState([]);
  const [clinics, setClinics] = useState([]);
  const [shifts, setShifts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('doctors'); // 'doctors' | 'shifts' | 'specialties'

  const { toastSuccess, toastError } = useToast();

  const loadData = async () => {
    setLoading(true);
    try {
      const [docs, specs, rms, shs] = await Promise.all([
        clinicService.getDoctors(),
        clinicService.getSpecialties(),
        clinicService.getClinics(),
        clinicService.getShifts(),
      ]);
      setDoctors(docs || []);
      setSpecialties(specs || []);
      setClinics(rms || []);
      setShifts(shs || []);
    } catch (err) {
      console.error('Failed to load doctor shifts data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Stethoscope className="w-6 h-6 text-medical-600" />
            Bác sĩ, Chuyên khoa & Ca làm việc (Shifts)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Quản lý hồ sơ bác sĩ, phân công phòng khám và lịch trực ca định kỳ
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-200 text-xs">
        <button
          onClick={() => setActiveTab('doctors')}
          className={`px-4 py-2.5 font-bold border-b-2 transition-colors ${
            activeTab === 'doctors'
              ? 'border-medical-600 text-medical-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Danh sách Bác sĩ ({doctors.length})
        </button>

        <button
          onClick={() => setActiveTab('shifts')}
          className={`px-4 py-2.5 font-bold border-b-2 transition-colors ${
            activeTab === 'shifts'
              ? 'border-medical-600 text-medical-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Ca làm việc / Lịch trực ({shifts.length})
        </button>

        <button
          onClick={() => setActiveTab('specialties')}
          className={`px-4 py-2.5 font-bold border-b-2 transition-colors ${
            activeTab === 'specialties'
              ? 'border-medical-600 text-medical-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          Chuyên khoa & Phòng khám ({specialties.length})
        </button>
      </div>

      {/* Tab Content: Doctors */}
      {activeTab === 'doctors' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {doctors.map((doc) => (
            <div
              key={doc.id}
              className="bg-white rounded-3xl border border-slate-200 p-5 shadow-2xs space-y-3"
            >
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-medical-50 text-medical-700 border border-medical-200 flex items-center justify-center font-bold text-base shadow-xs">
                  {doc.user?.full_name?.charAt(0) || 'BS'}
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-sm">{doc.user?.full_name}</h3>
                  <p className="text-[11px] text-slate-500">{doc.qualifications || 'Bác sĩ chuyên khoa'}</p>
                </div>
              </div>

              <div className="space-y-1.5 text-xs text-slate-600 pt-2 border-t border-slate-100">
                <div className="flex justify-between">
                  <span className="text-slate-400">Chuyên khoa:</span>
                  <strong className="text-slate-800">{doc.specialty?.name || 'Đa khoa'}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Phòng khám:</span>
                  <strong className="text-medical-700 font-semibold">{doc.clinic?.room_number || 'P101'}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Kinh nghiệm:</span>
                  <span>{doc.experience_years || 10} năm</span>
                </div>
              </div>

              <div className="pt-2">
                <span className="inline-block w-full py-1 text-center bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-xl text-[10px] font-bold">
                  ● Đang trong ca trực
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab Content: Shifts */}
      {activeTab === 'shifts' && (
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Bác sĩ phụ trách</th>
                <th className="py-3.5 px-4">Phòng khám</th>
                <th className="py-3.5 px-4">Ca trực</th>
                <th className="py-3.5 px-4">Khung giờ</th>
                <th className="py-3.5 px-4">Số lượng tiếp nhận tối đa</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {shifts.length === 0 ? (
                <tr>
                  <td colSpan="5" className="py-8 text-center text-slate-400 italic">
                    Chưa có lịch trực ca nào được thiết lập
                  </td>
                </tr>
              ) : (
                shifts.map((sh) => (
                  <tr key={sh.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-bold text-slate-900">
                      {sh.doctor?.user?.full_name || `Bác sĩ #${sh.doctor_id}`}
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-medical-700">
                      Phòng {sh.clinic?.room_number || 'P101'}
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-sky-50 text-sky-800 border border-sky-200">
                        {sh.shift_type || 'Ca ngày'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-mono font-medium text-slate-700">
                      {formatTime(sh.start_time)} - {formatTime(sh.end_time)}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-slate-900 font-mono">
                      {sh.max_patients || 30} lượt BN
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab Content: Specialties */}
      {activeTab === 'specialties' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {specialties.map((spec) => (
            <div
              key={spec.id}
              className="bg-white rounded-3xl border border-slate-200 p-5 shadow-2xs space-y-2"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                  {spec.code}
                </span>
                <Building className="w-4 h-4 text-medical-600" />
              </div>
              <h3 className="font-bold text-slate-900 text-sm">{spec.name}</h3>
              <p className="text-[11px] text-slate-500 leading-relaxed">{spec.description || 'Chuyên khoa khám lâm sàng và điều trị'}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DoctorShiftPage;
