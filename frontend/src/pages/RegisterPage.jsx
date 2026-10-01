import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const fieldClass = 'w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 focus:border-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-200';

const RegisterPage = () => {
  const [form, setForm] = useState({ full_name: '', username: '', email: '', role: 'receptionist', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const update = (event) => setForm({
    ...form,
    [event.target.name]: event.target.name === 'username'
      ? event.target.value.toLowerCase()
      : event.target.value,
  });

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    if (form.password !== form.confirmPassword) {
      setError('Mật khẩu xác nhận không khớp.');
      return;
    }
    setLoading(true);
    try {
      await api.post('/auth/register', {
        full_name: form.full_name,
        username: form.username,
        email: form.email,
        role: form.role,
        password: form.password,
      });
      setSubmitted(true);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Không thể gửi đăng ký. Vui lòng kiểm tra thông tin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-900">
      <div className="mx-auto max-w-lg rounded-xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
        <p className="text-xs font-bold uppercase tracking-wider text-sky-700">Smart Clinic ICTU</p>
        <h1 className="mt-2 text-2xl font-bold tracking-tight">Đăng ký tài khoản nhân viên</h1>
        <p className="mt-2 text-sm text-slate-600">Tài khoản cần được quản trị viên kích hoạt trước khi đăng nhập.</p>

        {submitted ? (
          <div role="status" className="mt-6 rounded-lg border border-emerald-300 bg-emerald-50 p-4 text-sm text-emerald-900">
            Đã gửi đăng ký. Vui lòng chờ quản trị viên kích hoạt tài khoản của bạn.
          </div>
        ) : (
          <form onSubmit={submit} className="mt-6 space-y-4">
            <label className="block text-sm font-medium">Họ và tên
              <input className={`${fieldClass} mt-1`} name="full_name" value={form.full_name} onChange={update} required minLength={2} maxLength={100} autoComplete="name" />
            </label>
            <label className="block text-sm font-medium">Tên đăng nhập
              <input className={`${fieldClass} mt-1`} name="username" value={form.username} onChange={update} required minLength={3} maxLength={50} pattern="[A-Za-z0-9_]+" autoComplete="username" />
            </label>
            <label className="block text-sm font-medium">Email
              <input className={`${fieldClass} mt-1`} name="email" type="email" value={form.email} onChange={update} required maxLength={100} autoComplete="email" />
            </label>
            <label className="block text-sm font-medium">Vị trí công tác
              <select className={`${fieldClass} mt-1`} name="role" value={form.role} onChange={update}>
                <option value="receptionist">Lễ tân</option>
                <option value="doctor">Bác sĩ</option>
                <option value="accountant">Thu ngân / Kế toán</option>
              </select>
            </label>
            <label className="block text-sm font-medium">Mật khẩu
              <input className={`${fieldClass} mt-1`} name="password" type="password" value={form.password} onChange={update} required minLength={8} autoComplete="new-password" />
            </label>
            <label className="block text-sm font-medium">Xác nhận mật khẩu
              <input className={`${fieldClass} mt-1`} name="confirmPassword" type="password" value={form.confirmPassword} onChange={update} required minLength={8} autoComplete="new-password" />
            </label>
            {error && <p role="alert" className="rounded-lg bg-rose-50 p-3 text-sm text-rose-800">{error}</p>}
            <button disabled={loading} className="w-full rounded-lg bg-sky-700 px-4 py-2.5 text-sm font-bold text-white hover:bg-sky-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-600 disabled:opacity-50">
              {loading ? 'Đang gửi...' : 'Gửi đăng ký'}
            </button>
          </form>
        )}
        <div className="mt-6 flex flex-wrap gap-4 text-sm font-semibold text-sky-700">
          <Link to="/login" className="hover:underline">Về trang đăng nhập</Link>
          <Link to="/book-appointment" className="hover:underline">Đăng ký khám bệnh</Link>
        </div>
      </div>
    </main>
  );
};

export default RegisterPage;
