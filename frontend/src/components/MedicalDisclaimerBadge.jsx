import React from 'react';
import { ShieldAlert, ShieldCheck } from 'lucide-react';

const MedicalDisclaimerBadge = ({ className = '', compact = false, showPiiRedacted = true }) => {
  if (compact) {
    return (
      <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 bg-amber-50/80 border border-amber-200/80 rounded-lg text-[11px] font-medium text-amber-900 backdrop-blur-xs ${className}`}>
        <ShieldAlert className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
        <span className="leading-tight">
          <strong className="font-semibold">Miễn trừ y tế:</strong> Hỗ trợ hành chính — không thay thế bác sĩ.
        </span>
      </div>
    );
  }

  return (
    <div className={`p-3.5 bg-amber-50/70 border border-amber-200/80 rounded-xl text-xs text-amber-900 flex items-start gap-3 shadow-subtle backdrop-blur-xs ${className}`}>
      <div className="p-1.5 rounded-lg bg-amber-100/80 text-amber-700 flex-shrink-0 mt-0.5">
        <ShieldAlert className="w-4 h-4" />
      </div>
      <div className="space-y-1 leading-relaxed flex-1">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <span className="font-bold uppercase tracking-wider text-[10px] text-amber-950 flex items-center gap-1.5">
            Cảnh báo an toàn y tế & Giới hạn AI
          </span>
          {showPiiRedacted && (
            <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-mono font-bold bg-emerald-100/80 text-emerald-800 border border-emerald-200/60">
              <ShieldCheck className="w-3 h-3 text-emerald-600" />
              PII DE-IDENTIFIED
            </span>
          )}
        </div>
        <p className="text-[11px] text-amber-900/90 leading-normal">
          Nội dung do Trợ lý AI tổng hợp mang tính chất hỗ trợ thủ tục và đối chiếu tiền sử. Mọi chỉ định xét nghiệm, chẩn đoán ICD-10 và kê đơn thuốc bắt buộc do <strong>Bác sĩ phụ trách chuyên môn</strong> trực tiếp quyết định.
        </p>
      </div>
    </div>
  );
};

export default MedicalDisclaimerBadge;
