import React from 'react';
import { X, Printer, CheckCircle, QrCode, Building2, Phone, MapPin } from 'lucide-react';
import { formatCurrency, formatDateTime, formatDate } from '../utils/formatters';

const InvoicePrintModal = ({ isOpen, onClose, invoice, patient, items = [], onPrint = null }) => {
  if (!isOpen || !invoice) return null;

  const handlePrint = () => {
    if (onPrint) {
      onPrint();
    } else {
      window.print();
    }
  };

  const patientName = patient?.full_name || invoice.patient?.full_name || 'Bệnh nhân';
  const medicalCode = patient?.medical_code || invoice.patient?.medical_code || 'BN-N/A';
  const phone = patient?.phone || invoice.patient?.phone || '---';
  const insuranceNo = patient?.insurance_number || invoice.patient?.insurance_number || 'Không có';
  const address = patient?.address || invoice.patient?.address || 'Việt Nam';
  const consultationFee = invoice.consultation_fee || 150000;
  const serviceFee = invoice.service_fee || 0;
  const medicineFee = invoice.medicine_fee || 0;
  const totalAmount = invoice.total_amount || (consultationFee + serviceFee + medicineFee);
  const insuranceDiscount = invoice.insurance_discount || 0;
  const patientPay = invoice.patient_pay_amount || Math.max(0, totalAmount - insuranceDiscount);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header bar (no-print) */}
        <div className="px-6 py-4 bg-slate-800 text-white flex items-center justify-between no-print">
          <div className="flex items-center gap-2">
            <Printer className="w-5 h-5 text-medical-400" />
            <h3 className="font-semibold text-lg">Hóa đơn thu tiền / Phiếu thanh toán viện phí</h3>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-4 py-2 bg-medical-600 hover:bg-medical-500 text-white text-sm font-medium rounded-lg shadow transition-colors"
            >
              <Printer className="w-4 h-4" />
              In phiếu (Ctrl+P)
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Printable Receipt Paper Container */}
        <div className="overflow-y-auto p-8 bg-slate-100 flex-1 flex justify-center">
          <div
            id="printable-invoice"
            className="bg-white text-slate-800 p-8 rounded-xl shadow border border-slate-200 w-full max-w-2xl font-sans text-sm"
          >
            {/* Clinic Branding Header */}
            <div className="flex items-start justify-between border-b border-slate-300 pb-4 mb-6">
              <div>
                <div className="flex items-center gap-2 text-medical-700 font-bold text-lg uppercase tracking-tight">
                  <Building2 className="w-6 h-6 text-medical-600" />
                  PHÒNG KHÁM ĐA KHOA THÔNG MINH ICTU
                </div>
                <div className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5" />
                  Đường Z115, Xã Quyết Thắng, TP. Thái Nguyên
                </div>
                <div className="text-xs text-slate-500 mt-0.5 flex items-center gap-1">
                  <Phone className="w-3.5 h-3.5" />
                  Hotline tiếp đón: 1900 8888 - 0208 3846 123
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-slate-400 uppercase tracking-widest font-semibold">Mẫu số: 01/BV-PK</div>
                <div className="text-sm font-bold text-slate-900 mt-1">Mã HĐ: {invoice.invoice_code || 'HD-TEMP'}</div>
                <div className="text-xs text-slate-500">Ngày: {formatDateTime(invoice.created_at || new Date().toISOString())}</div>
              </div>
            </div>

            {/* Document Title */}
            <div className="text-center my-4">
              <h1 className="text-xl font-extrabold text-slate-900 uppercase tracking-wide">
                HÓA ĐƠN THU TIỀN VIỆN PHÍ & DỊCH VỤ Y TẾ
              </h1>
              <p className="text-xs text-slate-500 italic mt-0.5">
                (Kèm theo Bảng kê chi phí khám, xét nghiệm và thuốc điều trị)
              </p>
            </div>

            {/* Patient Info Grid */}
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 mb-6 grid grid-cols-2 gap-y-2 text-xs">
              <div><span className="text-slate-500">Họ và tên bệnh nhân:</span> <strong className="text-slate-900 text-sm font-bold">{patientName}</strong></div>
              <div><span className="text-slate-500">Mã bệnh nhân:</span> <strong className="text-medical-700 font-mono font-semibold">{medicalCode}</strong></div>
              <div><span className="text-slate-500">Số điện thoại:</span> <span className="text-slate-800">{phone}</span></div>
              <div><span className="text-slate-500">Thẻ BHYT:</span> <span className="text-slate-800 font-mono font-semibold">{insuranceNo}</span></div>
              <div className="col-span-2"><span className="text-slate-500">Địa chỉ:</span> <span className="text-slate-800">{address}</span></div>
            </div>

            {/* Itemized Table */}
            <table className="w-full text-xs border-collapse mb-6">
              <thead>
                <tr className="bg-slate-100 border-y border-slate-300 text-slate-700">
                  <th className="py-2.5 px-3 text-left font-semibold">STT</th>
                  <th className="py-2.5 px-3 text-left font-semibold">Hạng mục chi phí / Dịch vụ</th>
                  <th className="py-2.5 px-3 text-center font-semibold">ĐVT</th>
                  <th className="py-2.5 px-3 text-right font-semibold">Thành tiền (VNĐ)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                <tr>
                  <td className="py-2.5 px-3 text-slate-500">1</td>
                  <td className="py-2.5 px-3 font-medium text-slate-800">Khám lâm sàng chuyên khoa</td>
                  <td className="py-2.5 px-3 text-center text-slate-500">Lượt</td>
                  <td className="py-2.5 px-3 text-right font-medium">{formatCurrency(consultationFee)}</td>
                </tr>
                {serviceFee > 0 && (
                  <tr>
                    <td className="py-2.5 px-3 text-slate-500">2</td>
                    <td className="py-2.5 px-3 font-medium text-slate-800">Chỉ định xét nghiệm / Chẩn đoán hình ảnh</td>
                    <td className="py-2.5 px-3 text-center text-slate-500">Gói</td>
                    <td className="py-2.5 px-3 text-right font-medium">{formatCurrency(serviceFee)}</td>
                  </tr>
                )}
                {medicineFee > 0 && (
                  <tr>
                    <td className="py-2.5 px-3 text-slate-500">3</td>
                    <td className="py-2.5 px-3 font-medium text-slate-800">Thuốc theo đơn điện tử</td>
                    <td className="py-2.5 px-3 text-center text-slate-500">Đơn</td>
                    <td className="py-2.5 px-3 text-right font-medium">{formatCurrency(medicineFee)}</td>
                  </tr>
                )}
              </tbody>
            </table>

            {/* Financial Summary */}
            <div className="border-t-2 border-slate-300 pt-3 space-y-1.5 text-xs">
              <div className="flex justify-between text-slate-600">
                <span>Tổng chi phí dịch vụ:</span>
                <span className="font-semibold text-slate-900">{formatCurrency(totalAmount)}</span>
              </div>
              <div className="flex justify-between text-emerald-700">
                <span>Bảo hiểm y tế (BHYT) chi trả:</span>
                <span className="font-semibold">- {formatCurrency(insuranceDiscount)}</span>
              </div>
              <div className="flex justify-between text-sm font-extrabold text-medical-800 border-t border-slate-200 pt-2">
                <span>SỐ TIỀN BỆNH NHÂN PHẢI THANH TOÁN:</span>
                <span className="text-base text-medical-700">{formatCurrency(patientPay)}</span>
              </div>
              <div className="flex justify-between text-slate-500 text-[11px] pt-1">
                <span>Phương thức thanh toán:</span>
                <span className="font-semibold text-slate-800 uppercase">
                  {invoice.payment_method === 'BANK_TRANSFER' ? 'Chuyển khoản / VietQR' : invoice.payment_method === 'INSURANCE' ? 'Bảo lãnh viện phí' : 'Tiền mặt'}
                </span>
              </div>
              <div className="flex justify-between text-slate-500 text-[11px]">
                <span>Trạng thái:</span>
                <span className="font-bold text-emerald-700 uppercase">
                  {invoice.payment_status === 'PAID' ? 'ĐÃ HOÀN TẤT THANH TOÁN' : 'CHỜ THANH TOÁN'}
                </span>
              </div>
            </div>

            {/* VietQR & Signature Footer */}
            <div className="mt-8 pt-4 border-t border-slate-200 grid grid-cols-3 gap-4 text-center text-xs">
              <div className="flex flex-col items-center">
                <div className="p-2 border border-slate-200 rounded-lg bg-slate-50">
                  <QrCode className="w-14 h-14 text-slate-800" />
                </div>
                <span className="text-[10px] text-slate-500 mt-1">Mã xác thực hóa đơn</span>
              </div>
              <div>
                <p className="font-bold text-slate-800">Người nộp tiền</p>
                <p className="text-[10px] text-slate-400 italic mt-0.5">(Ký và ghi rõ họ tên)</p>
                <div className="h-12"></div>
                <p className="font-medium text-slate-700">{patientName}</p>
              </div>
              <div>
                <p className="font-bold text-slate-800">Thu ngân / Kế toán</p>
                <p className="text-[10px] text-slate-400 italic mt-0.5">(Ký, đóng dấu thu tiền)</p>
                <div className="h-12"></div>
                <p className="font-medium text-slate-700">{invoice.cashier?.full_name || 'Trần Bích Phương'}</p>
              </div>
            </div>

            {/* Legal watermark notice */}
            <div className="mt-6 text-center text-[10px] text-slate-400 border-t border-dotted border-slate-200 pt-2">
              Phiếu thu điện tử hợp lệ được xuất từ Hệ thống Quản lý Y tế Đa khoa ICTU. Quý khách vui lòng giữ phiếu để đối chiếu khi cần thiết.
            </div>
          </div>
        </div>

        {/* Footer actions (no-print) */}
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end gap-3 no-print">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 text-sm font-medium rounded-lg transition-colors"
          >
            Đóng
          </button>
          <button
            onClick={handlePrint}
            className="flex items-center gap-1.5 px-5 py-2 bg-medical-600 hover:bg-medical-700 text-white text-sm font-medium rounded-lg shadow transition-colors"
          >
            <Printer className="w-4 h-4" />
            In phiếu thu ngay
          </button>
        </div>
      </div>
    </div>
  );
};

export default InvoicePrintModal;
