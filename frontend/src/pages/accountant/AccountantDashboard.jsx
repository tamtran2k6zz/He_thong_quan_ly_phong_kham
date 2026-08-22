import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  CreditCard,
  DollarSign,
  TrendingUp,
  Receipt,
  CheckCircle2,
  Clock,
  QrCode,
  Shield,
  Search,
  ArrowRight,
  Printer
} from 'lucide-react';
import { statsService } from '../../services/statsService';
import { invoiceService } from '../../services/invoiceService';
import { useToast } from '../../context/ToastContext';
import { formatCurrency, formatDateTime, getPaymentStatusInfo } from '../../utils/formatters';

const AccountantDashboard = () => {
  const [revenueStats, setRevenueStats] = useState(null);
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const loadData = async () => {
    setLoading(true);
    try {
      const [stats, invs] = await Promise.all([
        statsService.getRevenueStats(),
        invoiceService.getInvoices({ limit: 50 }),
      ]);
      setRevenueStats(stats);
      setInvoices(invs || [
        {
          id: 1,
          invoice_code: 'HD-20260822-0001',
          patient: { full_name: 'Trần Minh Đức', medical_code: 'BN-20260822-0001', phone: '0988123456' },
          consultation_fee: 150000,
          service_fee: 165000,
          medicine_fee: 85000,
          total_amount: 400000,
          insurance_discount: 320000,
          patient_pay_amount: 80000,
          payment_status: 'PENDING',
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          invoice_code: 'HD-20260822-0002',
          patient: { full_name: 'Nguyễn Thị Mai', medical_code: 'BN-20260822-0002', phone: '0912345678' },
          consultation_fee: 150000,
          service_fee: 220000,
          medicine_fee: 140000,
          total_amount: 510000,
          insurance_discount: 0,
          patient_pay_amount: 510000,
          payment_status: 'PAID',
          payment_method: 'BANK_TRANSFER',
          paid_at: new Date().toISOString(),
          created_at: new Date().toISOString(),
        }
      ]);
    } catch (err) {
      console.error('Failed to load accountant stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const pendingInvoices = invoices.filter(i => i.payment_status === 'PENDING');
  const paidInvoices = invoices.filter(i => i.payment_status === 'PAID');

  const filteredInvoices = invoices.filter(inv => {
    if (!searchTerm) return true;
    const q = searchTerm.toLowerCase();
    return (
      inv.invoice_code?.toLowerCase().includes(q) ||
      inv.patient?.full_name?.toLowerCase().includes(q) ||
      inv.patient?.medical_code?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-amber-600 via-amber-700 to-orange-700 p-6 rounded-3xl text-white shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-xs font-semibold mb-2">
            <CreditCard className="w-3.5 h-3.5 text-amber-200" />
            Bộ phận Thu ngân & Kế toán Viện phí
          </div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
            Quản lý Viện phí & Thu tiền tự động
          </h1>
          <p className="text-xs text-amber-100 mt-1">
            Tổng hợp viện phí khám, xét nghiệm cận lâm sàng, thuốc và thanh toán VietQR / BHYT
          </p>
        </div>

        <Link
          to="/accountant/invoices"
          className="flex items-center gap-2 px-5 py-3 bg-white text-amber-900 font-bold text-xs rounded-2xl shadow-md hover:bg-amber-50 transition-all self-start sm:self-auto"
        >
          <Receipt className="w-4 h-4 text-amber-600" />
          Thu tiền viện phí ngay ({pendingInvoices.length} chờ)
        </Link>
      </div>

      {/* Revenue Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Tổng doanh thu tích lũy</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-2">
            {formatCurrency(revenueStats?.total_revenue || 36900000)}
          </div>
          <div className="text-[11px] text-slate-400 mt-1">Doanh thu toàn viện</div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-emerald-200 bg-emerald-50/20 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-emerald-800">Thực thu từ bệnh nhân</span>
            <div className="p-2 bg-emerald-100 text-emerald-600 rounded-xl">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-emerald-900 mt-2">
            {formatCurrency(revenueStats?.patient_paid_amount || 25700000)}
          </div>
          <div className="text-[11px] text-emerald-700 mt-1">Đã hoàn tất thanh toán</div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-sky-200 bg-sky-50/20 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-sky-800">BHYT chi trả bảo lãnh</span>
            <div className="p-2 bg-sky-100 text-sky-600 rounded-xl">
              <Shield className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-sky-900 mt-2">
            {formatCurrency(revenueStats?.insurance_covered_amount || 11200000)}
          </div>
          <div className="text-[11px] text-sky-700 mt-1">Quyết toán bảo hiểm y tế</div>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-amber-200 bg-amber-50/20 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-amber-800">Chờ thu tiền (Pending)</span>
            <div className="p-2 bg-amber-100 text-amber-600 rounded-xl">
              <Clock className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-amber-900 mt-2">
            {formatCurrency(revenueStats?.pending_amount || 1800000)}
          </div>
          <div className="text-[11px] text-amber-700 mt-1">{pendingInvoices.length} phiếu chờ thu</div>
        </div>
      </div>

      {/* Invoices List Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
        <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="font-bold text-slate-900 text-base">Danh sách hóa đơn viện phí gần đây</h2>
            <p className="text-xs text-slate-500">Tra cứu mã hóa đơn, thông tin bệnh nhân và trạng thái thanh toán</p>
          </div>

          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Tìm mã hóa đơn, bệnh nhân..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>
        </div>

        <div className="overflow-x-auto flex-1">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Mã hóa đơn / Ngày</th>
                <th className="py-3.5 px-4">Bệnh nhân / Mã BN</th>
                <th className="py-3.5 px-4">Tổng chi phí</th>
                <th className="py-3.5 px-4">BHYT giảm trừ</th>
                <th className="py-3.5 px-4">BN Thực trả</th>
                <th className="py-3.5 px-4">Trạng thái</th>
                <th className="py-3.5 px-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredInvoices.map((inv) => {
                const statusInfo = getPaymentStatusInfo(inv.payment_status);
                return (
                  <tr key={inv.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-mono">
                      <span className="font-bold text-slate-900">{inv.invoice_code}</span>
                      <div className="text-[11px] text-slate-400">{formatDateTime(inv.created_at)}</div>
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="font-bold text-slate-900">{inv.patient?.full_name || 'Bệnh nhân'}</div>
                      <div className="text-[11px] font-mono text-medical-700 font-semibold">{inv.patient?.medical_code || '---'}</div>
                    </td>

                    <td className="py-3.5 px-4 font-medium text-slate-700">
                      {formatCurrency(inv.total_amount)}
                    </td>

                    <td className="py-3.5 px-4 text-emerald-700 font-semibold">
                      - {formatCurrency(inv.insurance_discount)}
                    </td>

                    <td className="py-3.5 px-4 font-bold text-amber-900 text-sm">
                      {formatCurrency(inv.patient_pay_amount)}
                    </td>

                    <td className="py-3.5 px-4">
                      <span className={`inline-flex px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${statusInfo.color}`}>
                        {statusInfo.label}
                      </span>
                    </td>

                    <td className="py-3.5 px-4 text-right">
                      {inv.payment_status === 'PENDING' ? (
                        <button
                          onClick={() => navigate(`/accountant/invoices?invoice_id=${inv.id}`)}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-bold text-[11px] shadow-2xs transition-colors"
                        >
                          <CreditCard className="w-3.5 h-3.5" />
                          Thu tiền ngay
                        </button>
                      ) : (
                        <button
                          onClick={() => navigate(`/accountant/invoices?invoice_id=${inv.id}`)}
                          className="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold text-[11px] transition-colors"
                        >
                          <Printer className="w-3.5 h-3.5" />
                          In lại hóa đơn
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AccountantDashboard;
