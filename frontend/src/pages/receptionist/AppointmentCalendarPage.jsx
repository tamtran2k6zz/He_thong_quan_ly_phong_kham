import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Calendar as CalendarIcon,
  Clock,
  User,
  Stethoscope,
  Building,
  Plus,
  AlertCircle,
  CheckCircle2,
  X,
  Search,
  Filter,
  Check
} from 'lucide-react';
import { appointmentService } from '../../services/appointmentService';
import { clinicService } from '../../services/clinicService';
import { patientService } from '../../services/patientService';
import { useToast } from '../../context/ToastContext';
import { formatDate, formatTime, getAppointmentStatusInfo } from '../../utils/formatters';

const AppointmentCalendarPage = () => {
  const [searchParams] = useSearchParams();
  const initialPatientId = searchParams.get('patient_id');

  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [specialties, setSpecialties] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [selectedDoctorId, setSelectedDoctorId] = useState('');
  const [selectedSpecialtyId, setSelectedSpecialtyId] = useState('');
  const [loading, setLoading] = useState(true);
  const [slotsLoading, setSlotsLoading] = useState(false);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [conflictWarning, setConflictWarning] = useState(null);

  const { toastSuccess, toastError } = useToast();

  // Booking form state
  const [bookingForm, setBookingForm] = useState({
    patient_id: initialPatientId || '',
    doctor_id: '',
    clinic_id: '',
    appointment_date: selectedDate,
    start_time: '08:30:00',
    end_time: '09:00:00',
    reason: 'Khám lâm sàng định kỳ',
  });

  // Load baseline metadata
  useEffect(() => {
    const fetchBase = async () => {
      setLoading(true);
      try {
        const [specs, docs, pats] = await Promise.all([
          clinicService.getSpecialties(),
          clinicService.getDoctors(),
          patientService.getPatients('', 0, 100),
        ]);
        setSpecialties(specs || []);
        setDoctors(docs || []);
        setPatients(pats || []);
        if (docs && docs.length > 0) {
          setSelectedDoctorId(docs[0].id);
          setBookingForm((prev) => ({
            ...prev,
            doctor_id: docs[0].id,
            clinic_id: docs[0].clinic_id || '',
            patient_id: initialPatientId || (pats?.[0]?.id || '')
          }));
        }
      } catch (err) {
        console.error('Failed to load initial scheduling data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchBase();
  }, [initialPatientId]);

  // Load appointments for selected date
  const loadAppointments = async () => {
    try {
      const data = await appointmentService.getAppointments({
        appointment_date: selectedDate,
        doctor_id: selectedDoctorId || undefined,
      });
      setAppointments(data || []);
    } catch (err) {
      console.error('Failed to load appointments:', err);
    }
  };

  // Load available slots with conflict engine
  const loadSlots = async () => {
    if (!selectedDoctorId) return;
    setSlotsLoading(true);
    try {
      const slots = await appointmentService.getAvailableSlots(
        selectedDoctorId,
        selectedDate
      );
      setAvailableSlots(slots || []);
    } catch (err) {
      console.error('Failed to calculate available slots:', err);
    } finally {
      setSlotsLoading(false);
    }
  };

  useEffect(() => {
    loadAppointments();
    loadSlots();
  }, [selectedDate, selectedDoctorId]);

  const handleDoctorChange = (docId) => {
    setSelectedDoctorId(docId);
    const doc = doctors.find((d) => d.id === parseInt(docId));
    if (doc) {
      setBookingForm((prev) => ({
        ...prev,
        doctor_id: doc.id,
        clinic_id: doc.clinic_id || '',
      }));
    }
  };

  const handleSelectSlot = (slot) => {
    if (!slot.is_available) {
      setConflictWarning(`Khung giờ này đã bị xung đột: ${slot.conflict_reason}`);
      return;
    }
    setConflictWarning(null);
    setBookingForm((prev) => ({
      ...prev,
      appointment_date: selectedDate,
      start_time: slot.start_time,
      end_time: slot.end_time,
    }));
    setShowBookingModal(true);
  };

  const handleBookAppointment = async (e) => {
    e.preventDefault();
    if (!bookingForm.patient_id || !bookingForm.doctor_id) {
      toastError('Vui lòng chọn Bệnh nhân và Bác sĩ khám');
      return;
    }

    try {
      const created = await appointmentService.createAppointment({
        ...bookingForm,
        patient_id: parseInt(bookingForm.patient_id),
        doctor_id: parseInt(bookingForm.doctor_id),
        clinic_id: bookingForm.clinic_id ? parseInt(bookingForm.clinic_id) : undefined,
      });
      toastSuccess(`Đặt lịch thành công! Mã lịch hẹn: ${created.appointment_code}`);
      setShowBookingModal(false);
      loadAppointments();
      loadSlots();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Đặt lịch hẹn thất bại';
      toastError(msg);
      setConflictWarning(msg);
    }
  };

  const handleCheckIn = async (appointmentId, code) => {
    try {
      await appointmentService.checkInAppointment(appointmentId);
      toastSuccess(`Đã tiếp đón bệnh nhân (Mã LH: ${code})`);
      loadAppointments();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Tiếp đón thất bại');
    }
  };

  const handleConfirm = async (appointmentId, code) => {
    try {
      await appointmentService.updateAppointment(appointmentId, { status: 'CONFIRMED' });
      toastSuccess(`Đã xác nhận lịch hẹn ${code}`);
      loadAppointments();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Xác nhận lịch hẹn thất bại');
    }
  };

  const handleCancel = async (appointmentId, code) => {
    if (!window.confirm(`Xác nhận hủy lịch hẹn ${code}?`)) return;
    try {
      await appointmentService.cancelAppointment(appointmentId);
      toastSuccess(`Đã hủy lịch ${code}`);
      loadAppointments();
      loadSlots();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Hủy lịch thất bại');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
            Lịch khám & Đặt lịch hẹn tự động
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Tích hợp thuật toán phát hiện và ngăn ngừa trùng lịch Bác sĩ & Phòng khám
          </p>
        </div>

        <button
          onClick={() => {
            setConflictWarning(null);
            setShowBookingModal(true);
          }}
          className="flex items-center gap-1.5 px-4 py-2.5 bg-medical-600 hover:bg-medical-700 text-white rounded-xl text-xs font-bold shadow-md transition-colors self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          Đặt lịch khám mới
        </button>
      </div>

      {/* Date & Doctor Selection Bar */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200 shadow-sm grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
        <div>
          <label className="block font-bold text-slate-700 mb-1.5 flex items-center gap-1.5">
            <CalendarIcon className="w-4 h-4 text-medical-600" />
            Chọn ngày khám
          </label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:ring-2 focus:ring-medical-500"
          />
        </div>

        <div>
          <label className="block font-bold text-slate-700 mb-1.5 flex items-center gap-1.5">
            <Stethoscope className="w-4 h-4 text-medical-600" />
            Bác sĩ phụ trách
          </label>
          <select
            value={selectedDoctorId}
            onChange={(e) => handleDoctorChange(e.target.value)}
            className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:ring-2 focus:ring-medical-500"
          >
            {doctors.map((doc) => (
              <option key={doc.id} value={doc.id}>
                {doc.user?.full_name || `Bác sĩ #${doc.id}`} ({doc.specialty?.name || 'Đa khoa'})
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col justify-end">
          <div className="p-2.5 bg-sky-50 border border-sky-200 rounded-xl text-[11px] text-sky-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-sky-600 flex-shrink-0" />
            <span>Phát hiện xung đột tự động theo thời gian thực</span>
          </div>
        </div>
      </div>

      {/* Main Content: Time Slots Matrix & Appointments List */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Available Time Slots Grid (5 cols) */}
        <div className="lg:col-span-5 bg-white rounded-3xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="font-bold text-slate-900 text-sm">Khung giờ khám trong ngày</h3>
              <p className="text-[11px] text-slate-400">Chọn khung giờ trống (màu xanh) để đặt nhanh</p>
            </div>
            <div className="text-[10px] font-bold px-2 py-0.5 bg-slate-100 text-slate-600 rounded-full">
              30 phút / lượt
            </div>
          </div>

          {slotsLoading ? (
            <div className="py-12 text-center text-slate-400 italic text-xs">
              Đang kiểm tra tình trạng trùng lịch...
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2.5">
              {availableSlots.map((slot, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelectSlot(slot)}
                  className={`p-3 rounded-2xl border text-left transition-all relative ${
                    slot.is_available
                      ? 'bg-emerald-50/70 border-emerald-300 hover:bg-emerald-100 text-emerald-950 hover:shadow-xs cursor-pointer'
                      : 'bg-rose-50/70 border-rose-200 text-rose-900 opacity-80 cursor-not-allowed'
                  }`}
                  title={slot.is_available ? 'Khung giờ còn trống' : `Trùng lịch: ${slot.conflict_reason}`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs font-mono">
                      {formatTime(slot.start_time)} - {formatTime(slot.end_time)}
                    </span>
                    {slot.is_available ? (
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    ) : (
                      <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                    )}
                  </div>
                  <div className="text-[10px] mt-1 truncate">
                    {slot.is_available ? '✓ Còn trống' : `✕ ${slot.conflict_reason || 'Đã có lịch'}`}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Booked Appointments on Selected Date (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-3xl border border-slate-200 shadow-sm p-5 space-y-4 flex flex-col">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                Danh sách lịch đã đặt ({formatDate(selectedDate)})
              </h3>
              <p className="text-[11px] text-slate-400">Tổng cộng {appointments.length} ca khám</p>
            </div>
          </div>

          <div className="space-y-3 overflow-y-auto max-h-[500px] flex-1">
            {appointments.length === 0 ? (
              <div className="py-16 text-center text-slate-400 italic text-xs">
                Chưa có lịch hẹn nào được ghi nhận trong ngày này
              </div>
            ) : (
              appointments.map((appt) => {
                const statusInfo = getAppointmentStatusInfo(appt.status);
                return (
                  <div
                    key={appt.id}
                    className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-300 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold font-mono text-medical-700 text-sm">
                          {appt.appointment_code}
                        </span>
                        <span className={`px-2 py-0.2 rounded-full text-[10px] font-bold border ${statusInfo.color}`}>
                          {statusInfo.label}
                        </span>
                      </div>

                      <div className="font-semibold text-slate-900 text-sm">
                        {appt.patient?.full_name || 'Bệnh nhân'}
                      </div>

                      <div className="text-slate-500 text-[11px] flex items-center gap-3">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3 text-slate-400" />
                          {formatTime(appt.start_time)} - {formatTime(appt.end_time)}
                        </span>
                        <span>• BS: {appt.doctor?.user?.full_name || 'Bác sĩ'}</span>
                        <span>• Phòng: {appt.clinic?.room_number || 'P101'}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 self-end sm:self-center">
                      {appt.status === 'PENDING' && (
                        <button
                          onClick={() => handleConfirm(appt.id, appt.appointment_code)}
                          className="flex items-center gap-1 rounded-lg border border-sky-300 bg-sky-50 px-3 py-1.5 text-[11px] font-bold text-sky-800 hover:bg-sky-100"
                        >
                          <CheckCircle2 className="h-3.5 w-3.5" /> Xác nhận
                        </button>
                      )}
                      {(appt.status === 'CONFIRMED' || appt.status === 'PENDING') && (
                        <button
                          onClick={() => handleCheckIn(appt.id, appt.appointment_code)}
                          className="flex items-center gap-1 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-[11px] shadow-2xs transition-colors"
                        >
                          <Check className="w-3.5 h-3.5" /> Tiếp đón
                        </button>
                      )}

                      {appt.status !== 'COMPLETED' && appt.status !== 'CANCELLED' && (
                        <button
                          onClick={() => handleCancel(appt.id, appt.appointment_code)}
                          className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors"
                          title="Hủy lịch hẹn"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* Booking Form Modal */}
      {showBookingModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-xl w-full p-6 sm:p-8 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-medical-500 text-white rounded-xl">
                  <CalendarIcon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">Đặt lịch khám bệnh</h3>
                  <p className="text-xs text-slate-500">Kiểm tra xung đột phòng khám & bác sĩ tự động</p>
                </div>
              </div>
              <button
                onClick={() => setShowBookingModal(false)}
                className="p-2 text-slate-400 hover:text-slate-600 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Live Conflict Alert Banner */}
            {conflictWarning && (
              <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-2xl flex items-start gap-2.5 text-rose-900 text-xs">
                <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <div>
                  <strong className="block font-bold">Cảnh báo trùng lịch khám!</strong>
                  <span>{conflictWarning}</span>
                </div>
              </div>
            )}

            <form onSubmit={handleBookAppointment} className="space-y-4 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">
                  Chọn bệnh nhân *
                </label>
                <select
                  required
                  value={bookingForm.patient_id}
                  onChange={(e) => setBookingForm({ ...bookingForm, patient_id: e.target.value })}
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
                >
                  <option value="">-- Chọn bệnh nhân --</option>
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.full_name} ({p.medical_code}) - SĐT: {p.phone}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Bác sĩ khám *
                  </label>
                  <select
                    required
                    value={bookingForm.doctor_id}
                    onChange={(e) => {
                      const docId = e.target.value;
                      const doc = doctors.find((d) => d.id === parseInt(docId));
                      setBookingForm({
                        ...bookingForm,
                        doctor_id: docId,
                        clinic_id: doc?.clinic_id || '',
                      });
                    }}
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
                  >
                    <option value="">-- Chọn bác sĩ --</option>
                    {doctors.map((doc) => (
                      <option key={doc.id} value={doc.id}>
                        {doc.user?.full_name || `Bác sĩ #${doc.id}`} ({doc.specialty?.name || 'Đa khoa'})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Ngày khám *
                  </label>
                  <input
                    type="date"
                    required
                    value={bookingForm.appointment_date}
                    onChange={(e) => setBookingForm({ ...bookingForm, appointment_date: e.target.value })}
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Giờ bắt đầu *
                  </label>
                  <input
                    type="time"
                    required
                    value={bookingForm.start_time}
                    onChange={(e) => setBookingForm({ ...bookingForm, start_time: e.target.value })}
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Giờ kết thúc *
                  </label>
                  <input
                    type="time"
                    required
                    value={bookingForm.end_time}
                    onChange={(e) => setBookingForm({ ...bookingForm, end_time: e.target.value })}
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">
                  Lý do khám / Triệu chứng ban đầu
                </label>
                <textarea
                  rows={2}
                  value={bookingForm.reason}
                  onChange={(e) => setBookingForm({ ...bookingForm, reason: e.target.value })}
                  placeholder="Ví dụ: Đau đầu, sốt nhẹ 2 ngày nay..."
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowBookingModal(false)}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-medical-600 hover:bg-medical-700 text-white font-bold rounded-xl shadow-md transition-colors"
                >
                  Xác nhận đặt lịch
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AppointmentCalendarPage;
