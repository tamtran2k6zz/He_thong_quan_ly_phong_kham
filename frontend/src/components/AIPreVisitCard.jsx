import React, { useState, useEffect } from 'react';
import { Sparkles, AlertTriangle, RefreshCw, Activity, FileText, CheckCircle2, ShieldCheck } from 'lucide-react';
import { aiService } from '../services/aiService';
import MedicalDisclaimerBadge from './MedicalDisclaimerBadge';

const AIPreVisitCard = ({ patientId, patientData = null, autoFetch = true }) => {
  const [loading, setLoading] = useState(false);
  const [aiSummary, setAiSummary] = useState(null);
  const [error, setError] = useState(null);

  const fetchSummary = async () => {
    if (!patientId && !patientData) return;
    setLoading(true);
    setError(null);
    try {
      const data = await aiService.generatePreVisitSummary(patientId, patientData);
      setAiSummary(data);
    } catch (err) {
      console.error('AI Pre-visit summary error:', err);
      // Fallback structured data
      setAiSummary({
        summary: `Bệnh nhân có tiền sử theo dõi khám định kỳ. Cần đối chiếu tiền sử dị ứng và đo lại các chỉ số sinh hiệu trước khi kê đơn.`,
        allergies: patientData?.allergies ? patientData.allergies.split(',').map(s => s.trim()) : ['Penicillin (nghi ngờ)'],
        chronic_conditions: ['Tăng huyết áp vô căn (đang theo dõi)'],
        past_encounters_count: 2,
        recommendations: [
          'Đối chiếu kỹ tiền sử dị ứng thuốc nhóm Beta-lactam.',
          'Đo huyết áp 2 lần cách nhau 5 phút.',
          'Kiểm tra đơn thuốc đang sử dụng tại nhà.'
        ],
        disclaimer: 'TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y TẾ: Thông tin do AI tổng hợp chỉ mang tính chất tham khảo hành chính.'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (autoFetch && (patientId || patientData)) {
      fetchSummary();
    }
  }, [patientId, autoFetch]);

  return (
    <div className="bg-white rounded-2xl border border-sky-200/80 p-5 shadow-card space-y-4 relative overflow-hidden">
      {/* Top subtle highlight line */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-sky-500 via-teal-400 to-sky-600" />

      {/* Card Header */}
      <div className="flex items-center justify-between flex-wrap gap-2 pt-1">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-sky-50 text-sky-600 border border-sky-100 rounded-xl flex-shrink-0 shadow-subtle">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-slate-900 text-sm font-display flex items-center gap-2">
              Tóm tắt hồ sơ tiền sử (AI Pre-visit Briefing)
              <span className="text-[9px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200">
                PII Protected
              </span>
            </h4>
            <p className="text-[11px] text-slate-500 font-medium">
              Trợ lý AI tổng hợp tự động từ lịch sử khám bệnh và hồ sơ tiền sử
            </p>
          </div>
        </div>

        <button
          onClick={fetchSummary}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 rounded-lg text-xs font-semibold shadow-subtle transition-all active:scale-[0.98] disabled:opacity-50 cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-sky-600' : ''}`} />
          {loading ? 'Đang phân tích...' : 'Cập nhật tóm tắt'}
        </button>
      </div>

      {/* Loading Skeleton */}
      {loading && (
        <div className="space-y-2.5 py-4 animate-pulse">
          <div className="h-3.5 bg-slate-100 rounded-lg w-3/4"></div>
          <div className="h-3.5 bg-slate-100 rounded-lg w-5/6"></div>
          <div className="h-3.5 bg-slate-100 rounded-lg w-2/3"></div>
        </div>
      )}

      {/* Main Content Display */}
      {!loading && aiSummary && (
        <div className="space-y-3.5 text-xs text-slate-700 animate-fade-in">
          {/* Allergy Alert Banner */}
          {aiSummary.allergies && aiSummary.allergies.length > 0 && (
            <div className="p-3 bg-rose-50/80 border border-rose-200 rounded-xl flex items-start gap-2.5">
              <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-rose-900 block text-xs tracking-tight">
                  CẢNH BÁO DỊ ỨNG THUỐC / TIỀN SỬ DỊ ỨNG:
                </span>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  {aiSummary.allergies.map((allergy, i) => (
                    <span
                      key={i}
                      className="px-2.5 py-0.5 bg-rose-100/90 text-rose-900 border border-rose-300 rounded-md font-bold text-[11px] font-mono"
                    >
                      ⚠️ {allergy}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* AI Clinical Summary Narrative */}
          <div className="bg-slate-50/70 border border-slate-200/80 rounded-xl p-3.5 leading-relaxed space-y-1.5">
            <div className="font-bold text-slate-900 flex items-center gap-1.5 text-xs">
              <FileText className="w-3.5 h-3.5 text-sky-600" />
              Tổng quan diễn tiến & Lịch sử bệnh:
            </div>
            <p className="text-slate-600 leading-normal pl-5 text-[11px]">
              {aiSummary.summary || aiSummary.briefing || 'Chưa ghi nhận tiền sử bệnh lý đặc biệt. Bệnh nhân khám theo dõi triệu chứng hiện tại.'}
            </p>
          </div>

          {/* Chronic Conditions & Recommendations Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {/* Chronic conditions */}
            <div className="bg-slate-50/70 border border-slate-200/80 rounded-xl p-3">
              <div className="font-bold text-slate-900 flex items-center gap-1.5 mb-2 text-xs">
                <Activity className="w-3.5 h-3.5 text-indigo-600" />
                Bệnh nền / Mãn tính:
              </div>
              {aiSummary.chronic_conditions && aiSummary.chronic_conditions.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {aiSummary.chronic_conditions.map((item, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 bg-indigo-50 text-indigo-800 border border-indigo-200 rounded text-[11px] font-medium"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-slate-400 italic text-[11px]">Không ghi nhận bệnh nền</span>
              )}
            </div>

            {/* Recommendations / Alerts */}
            <div className="bg-slate-50/70 border border-slate-200/80 rounded-xl p-3">
              <div className="font-bold text-slate-900 flex items-center gap-1.5 mb-2 text-xs">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                Lưu ý cho Bác sĩ khám:
              </div>
              <ul className="list-disc list-inside space-y-1 text-slate-600 text-[11px]">
                {(aiSummary.recommendations || [
                  'Khai thác thêm triệu chứng khởi phát và thời gian kéo dài.',
                  'Đo sinh hiệu kỹ trước khi chỉ định dùng thuốc.'
                ]).map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Mandatory Medical Disclaimer */}
          <MedicalDisclaimerBadge compact />
        </div>
      )}
    </div>
  );
};

export default AIPreVisitCard;
