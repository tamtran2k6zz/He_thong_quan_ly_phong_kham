import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const fieldClass = 'mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 focus:border-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-200';
const currentDate = new Date();
const today = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(currentDate.getDate()).padStart(2, '0')}`;

const toMinutes = (time) => {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
};

const formatTime = (minutes) => `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;

const BookAppointmentPage = () => {
  const [doctors, setDoctors] = useState([]);
  const [form, setForm] = useState({
    full_name: '', date_of_birth: '', gender: 'Nam', phone: '', identity_card: '',
    doctor_id: '', appointment_date: '', start_time: '', reason: '',
  });
  const [error, setError] = useState('');
  const [receipt, setReceipt] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.get('/public/doctors')
      .then((response) => setDoctors(response.data))
      .catch(() => setError('Không tải được danh sách bác sĩ. Vui lòng thử lại sau.'));
  }, []);

  const selectedDoctor = doctors.find((doctor) => String(doctor.id) === form.doctor_id);
  const slots = useMemo(() => {
    if (!selectedDoctor || !form.appointment_date) return [];
    const day = (new Date(`${form.appointment_date}T12:00:00`).getDay() + 6) % 7;
    const times = selectedDoctor.shifts
      .filter((shift) => shift.day_of_week === day)
      .flatMap((shift) => {
        const times = [];
        for (let minute = toMinutes(shift.start_time); minute + 30 <= toMinutes(shift.end_time); minute += 30) {
          times.push(formatTime(minute));
        }
        return times;
      });
    const now = new Date();
    const currentMinute = now.getHours() * 60 + now.getMinutes();
    return times.filter((slot) => form.appointment_date !== today || toMinutes(slot) > currentMinute);
  }, [selectedDoctor, form.appointment_date]);

  const update = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      [name]: value,
      ...(['doctor_id', 'appointment_date'].includes(name) ? { start_time: '' } : {}),
    }));
  };

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await api.post('/public/appointments', {
        ...form,
        doctor_id: Number(form.doctor_id),
        identity_card: form.identity_card || null,
        reason: form.reason || null,
      });
      setReceipt(response.data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Không thể đăng ký lịch khám. Vui lòng kiểm tra thông tin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-900">
      <div className="mx-auto max-w-2xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <p className="text-xs font-bold uppercase tracking-wider text-sky-700">Smart Clinic ICTU</p>
        <h1 className="mt-2 text-2xl font-bold tracking-tight">Đăng ký khám bệnh</h1>
        <p className="mt-2 text-sm text-slate-600">Chọn bác sĩ và giờ khám. Lịch hẹn sẽ ở trạng thái chờ xác nhận.</p>

        {receipt ? (
          <div role="status" className="mt-6 rounded-lg border border-emerald-300 bg-emerald-50 p-5 text-sm text-emerald-950">
            <p className="font-bold">Đã tiếp nhận đăng ký khám.</p>
            <p className="mt-2">Mã lịch hẹn: <strong className="font-mono tabular-nums">{receipt.appointment_code}</strong></p>
            <p className="mt-1">Ngày giờ: {receipt.appointment_date}, {receipt.start_time.slice(0, 5)}</p>
            <p className="mt-2">Vui lòng lưu mã lịch hẹn và liên hệ lễ tân để xác nhận lịch khám.</p>
          </div>
        ) : (
          <form onSubmit={submit} className="mt-6 grid gap-4 sm:grid-cols-2">
            <label className="block text-sm font-medium sm:col-span-2">Họ và tên bệnh nhân
              <input className={fieldClass} name="full_name" value={form.full_name} onChange={update} required minLength={2} maxLength={100} autoComplete="name" />
            </label>
            <label className="block text-sm font-medium">Ngày sinh
              <input className={fieldClass} name="date_of_birth" type="date" max={today} value={form.date_of_birth} onChange={update} required />
            </label>
            <label className="block text-sm font-medium">Giới tính
              <select className={fieldClass} name="gender" value={form.gender} onChange={update}>
                <option>Nam</option><option>Nữ</option><option>Khác</option>
              </select>
            </label>
            <label className="block text-sm font-medium">Số điện thoại
              <input className={fieldClass} name="phone" type="tel" value={form.phone} onChange={update} required pattern="(0[0-9]{9}|\+84[0-9]{9})" autoComplete="tel" />
            </label>
            <label className="block text-sm font-medium">CCCD (nếu có)
              <input className={fieldClass} name="identity_card" value={form.identity_card} onChange={update} pattern="[0-9]{12}" inputMode="numeric" />
            </label>
            <label className="block text-sm font-medium sm:col-span-2">Bác sĩ
              <select className={fieldClass} name="doctor_id" value={form.doctor_id} onChange={update} required>
                <option value="">Chọn bác sĩ</option>
                {doctors.map((doctor) => (
                  <option key={doctor.id} value={doctor.id}>{doctor.title} {doctor.full_name} — {doctor.specialty}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm font-medium">Ngày khám
              <input className={fieldClass} name="appointment_date" type="date" min={today} value={form.appointment_date} onChange={update} required />
            </label>
            <label className="block text-sm font-medium">Giờ khám
              <select className={fieldClass} name="start_time" value={form.start_time} onChange={update} required disabled={!slots.length}>
                <option value="">{slots.length ? 'Chọn giờ' : 'Không có ca làm việc'}</option>
                {slots.map((slot) => <option key={slot} value={slot}>{slot}</option>)}
              </select>
            </label>
            <label className="block text-sm font-medium sm:col-span-2">Lý do khám (không bắt buộc)
              <textarea className={fieldClass} name="reason" value={form.reason} onChange={update} maxLength={255} rows={3} />
            </label>
            {error && <p role="alert" className="rounded-lg bg-rose-50 p-3 text-sm text-rose-800 sm:col-span-2">{error}</p>}
            <button disabled={loading || !doctors.length} className="rounded-lg bg-sky-700 px-4 py-2.5 text-sm font-bold text-white hover:bg-sky-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-600 disabled:opacity-50 sm:col-span-2">
              {loading ? 'Đang gửi...' : 'Đăng ký lịch khám'}
            </button>
          </form>
        )}
        <div className="mt-6 flex flex-wrap gap-4 text-sm font-semibold text-sky-700">
          <Link to="/login" className="hover:underline">Về trang đăng nhập</Link>
          <Link to="/register" className="hover:underline">Đăng ký tài khoản nhân viên</Link>
        </div>
      </div>
    </main>
  );
};

export default BookAppointmentPage;
