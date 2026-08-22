import React from 'react';
import { ShieldAlert } from 'lucide-react';

const MedicalDisclaimerBadge = ({ className = '', compact = false }) => {
  if (compact) {
    return (
      <div className={`flex items-center gap-1.5 px-2.5 py-1 bg-amber-50 border border-amber-200 rounded-md text-[11px] font-medium text-amber-800 ${className}`}>
        <ShieldAlert className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
        <span>Tuyên bố miễn trừ: Nội dung AI chỉ mang tính tham khảo hành chính, không thay thế chẩn đoán y khoa.</span>
      </div>
    );
  }

  return (
    <div className={`p-3 bg-amber-50/90 border border-amber-200/80 rounded-lg text-xs text-amber-900 flex items-start gap-2.5 shadow-sm ${className}`}>
      <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
      <div className="leading-relaxed">
        <span className="font-semibold uppercase tracking-wider text-[11px] block text-amber-950 mb-0.5">
          Tuyên bố miễn trừ trách nhiệm y tế
        </span>
        Thông tin do Trợ lý AI tạo ra chỉ mang tính chất tham khảo hành chính và hỗ trợ thủ tục. Mọi quyết định chẩn đoán, phác đồ điều trị và kê đơn thuốc hoàn toàn thuộc thẩm quyền chuyên môn của Bác sĩ điều trị.
      </div>
    </div>
  );
};

export default MedicalDisclaimerBadge;
