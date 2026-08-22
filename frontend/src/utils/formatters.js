/**
 * Formatting and Helper Utilities for Medical Clinic Management
 */

export const formatCurrency = (amount) => {
  if (amount === undefined || amount === null || isNaN(amount)) return '0 ₫';
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    maximumFractionDigits: 0
  }).format(amount);
};

export const formatDate = (dateStr) => {
  if (!dateStr) return '---';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
  } catch {
    return dateStr;
  }
};

export const formatDateTime = (dateStr) => {
  if (!dateStr) return '---';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${hours}:${minutes} - ${day}/${month}/${year}`;
  } catch {
    return dateStr;
  }
};

export const formatTime = (timeStr) => {
  if (!timeStr) return '--:--';
  if (timeStr.length >= 5) return timeStr.substring(0, 5);
  return timeStr;
};

export const calculateBMI = (weightKg, heightCm) => {
  if (!weightKg || !heightCm || heightCm <= 0) {
    return { value: null, label: 'Chưa đủ dữ liệu', color: 'text-slate-500', bg: 'bg-slate-100' };
  }
  const heightM = heightCm / 100;
  const bmi = (weightKg / (heightM * heightM)).toFixed(1);
  const num = parseFloat(bmi);

  if (num < 18.5) {
    return { value: bmi, label: 'Thiếu cân', color: 'text-amber-700', bg: 'bg-amber-50 border-amber-200' };
  } else if (num < 23) {
    return { value: bmi, label: 'Bình thường (Chuẩn Châu Á)', color: 'text-emerald-700', bg: 'bg-emerald-50 border-emerald-200' };
  } else if (num < 25) {
    return { value: bmi, label: 'Tiền béo phì', color: 'text-orange-700', bg: 'bg-orange-50 border-orange-200' };
  } else {
    return { value: bmi, label: 'Béo phì', color: 'text-rose-700', bg: 'bg-rose-50 border-rose-200' };
  }
};

export const getRoleInfo = (role) => {
  switch (role?.toLowerCase()) {
    case 'admin':
      return { label: 'Quản trị viên', color: 'bg-purple-100 text-purple-800 border-purple-200' };
    case 'doctor':
      return { label: 'Bác sĩ', color: 'bg-blue-100 text-blue-800 border-blue-200' };
    case 'receptionist':
      return { label: 'Lễ tân tiếp đón', color: 'bg-emerald-100 text-emerald-800 border-emerald-200' };
    case 'accountant':
      return { label: 'Thu ngân / Kế toán', color: 'bg-amber-100 text-amber-800 border-amber-200' };
    default:
      return { label: role || 'Nhân viên', color: 'bg-slate-100 text-slate-800 border-slate-200' };
  }
};

export const getAppointmentStatusInfo = (status) => {
  switch (status?.toUpperCase()) {
    case 'PENDING':
      return { label: 'Chờ xác nhận', color: 'bg-amber-100 text-amber-800 border-amber-200' };
    case 'CONFIRMED':
      return { label: 'Đã xác nhận', color: 'bg-blue-100 text-blue-800 border-blue-200' };
    case 'CHECKED_IN':
      return { label: 'Đã tiếp đón (Chờ khám)', color: 'bg-emerald-100 text-emerald-800 border-emerald-200 animate-pulse' };
    case 'IN_PROGRESS':
      return { label: 'Đang khám', color: 'bg-indigo-100 text-indigo-800 border-indigo-200' };
    case 'COMPLETED':
      return { label: 'Đã hoàn tất', color: 'bg-slate-100 text-slate-700 border-slate-200' };
    case 'CANCELLED':
      return { label: 'Đã hủy', color: 'bg-rose-100 text-rose-800 border-rose-200' };
    default:
      return { label: status || 'Không rõ', color: 'bg-slate-100 text-slate-800 border-slate-200' };
  }
};

export const getPaymentStatusInfo = (status) => {
  switch (status?.toUpperCase()) {
    case 'PAID':
      return { label: 'Đã thanh toán', color: 'bg-emerald-100 text-emerald-800 border-emerald-300' };
    case 'PENDING':
      return { label: 'Chờ thanh toán', color: 'bg-amber-100 text-amber-800 border-amber-300' };
    case 'CANCELLED':
      return { label: 'Đã hủy', color: 'bg-rose-100 text-rose-800 border-rose-300' };
    default:
      return { label: status || 'Chưa thanh toán', color: 'bg-slate-100 text-slate-800 border-slate-300' };
  }
};
