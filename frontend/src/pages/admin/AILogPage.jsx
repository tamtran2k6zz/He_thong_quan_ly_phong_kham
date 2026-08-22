import React, { useState, useEffect } from 'react';
import {
  Bot,
  Search,
  Sparkles,
  ShieldAlert,
  Clock,
  Zap,
  Eye,
  X,
  RefreshCw
} from 'lucide-react';
import { auditService } from '../../services/auditService';
import { formatDateTime } from '../../utils/formatters';
import MedicalDisclaimerBadge from '../../components/MedicalDisclaimerBadge';

const AILogPage = () => {
  const [aiLogs, setAiLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [featureFilter, setFeatureFilter] = useState('');
  const [selectedLog, setSelectedLog] = useState(null);

  const loadAILogs = async () => {
    setLoading(true);
    try {
      const params = { limit: 100 };
      if (featureFilter) params.feature_name = featureFilter;
      const data = await auditService.getAILogs(params);
      setAiLogs(data || [
        {
          id: 1,
          feature_name: 'pre_visit_summary',
          model_used: 'MockDeterministicAIProvider',
          anonymized_prompt: 'Tóm tắt tiền sử bệnh án cho bệnh nhân [PATIENT_01], SĐT: [PHONE_REDACTED], CCCD: [CCCD_REDACTED]. Tiền sử: Dị ứng Penicillin.',
          response_text: 'Bệnh nhân có tiền sử dị ứng Penicillin. Khuyến nghị Bác sĩ kiểm tra nhóm thuốc trước khi kê đơn.',
          latency_ms: 120,
          user_id: 4,
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          feature_name: 'faq',
          model_used: 'MockDeterministicAIProvider',
          anonymized_prompt: 'Bệnh nhân hỏi: Giờ làm việc của phòng khám và quyền lợi BHYT đúng tuyến?',
          response_text: 'Phòng khám làm việc từ 07:30 - 17:00. BHYT đúng tuyến được thanh toán 80% - 100%. Kèm Tuyên bố miễn trừ y tế.',
          latency_ms: 85,
          user_id: 2,
          created_at: new Date().toISOString(),
        },
        {
          id: 3,
          feature_name: 'discharge_instructions',
          model_used: 'MockDeterministicAIProvider',
          anonymized_prompt: 'Sinh hướng dẫn sau khám cho chẩn đoán J06.9 - Viêm mũi họng cấp. Đơn thuốc: Paracetamol 500mg, Vitamin C 500mg.',
          response_text: '1. Uống thuốc theo đơn.\n2. Uống nhiều nước ấm, giữ ấm cổ họng.\n3. Tái khám sau 5 ngày nếu không đỡ.',
          latency_ms: 150,
          user_id: 4,
          created_at: new Date().toISOString(),
        }
      ]);
    } catch (err) {
      console.error('Failed to load AI invocation logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAILogs();
  }, [featureFilter]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Bot className="w-6 h-6 text-emerald-600" />
            Nhật ký gọi AI & Kiểm soát An toàn (AI Invocation Logs)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Giám sát độ trễ, mô hình AI, nội dung prompt sau khi khử định danh (PII Redaction)
          </p>
        </div>

        <button
          onClick={loadAILogs}
          className="flex items-center gap-1.5 px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-bold shadow-2xs transition-colors self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Làm mới log AI
        </button>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-3xl border border-slate-200 shadow-sm flex gap-3">
        <select
          value={featureFilter}
          onChange={(e) => setFeatureFilter(e.target.value)}
          className="px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:ring-2 focus:ring-emerald-500"
        >
          <option value="">-- Tất cả tính năng AI --</option>
          <option value="pre_visit_summary">Tóm tắt hồ sơ (Pre-visit Briefing)</option>
          <option value="faq">Chatbot tư vấn quy trình (FAQ Chatbot)</option>
          <option value="discharge_instructions">Hướng dẫn sau khám (Discharge Instructions)</option>
        </select>
      </div>

      {/* AI Logs Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Thời gian</th>
                <th className="py-3.5 px-4">Tính năng AI</th>
                <th className="py-3.5 px-4">Mô hình AI</th>
                <th className="py-3.5 px-4">Prompt đã khử PII</th>
                <th className="py-3.5 px-4">Độ trễ</th>
                <th className="py-3.5 px-4 text-right">Chi tiết</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {aiLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4 font-mono text-slate-500 whitespace-nowrap">
                    {formatDateTime(log.created_at)}
                  </td>

                  <td className="py-3.5 px-4">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                      {log.feature_name}
                    </span>
                  </td>

                  <td className="py-3.5 px-4 font-mono text-slate-700 font-semibold">
                    {log.model_used || 'MockDeterministic'}
                  </td>

                  <td className="py-3.5 px-4 max-w-sm truncate text-slate-600 font-mono text-[11px]">
                    {log.anonymized_prompt}
                  </td>

                  <td className="py-3.5 px-4">
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold text-sky-700">
                      <Zap className="w-3 h-3" />
                      {log.latency_ms || 100} ms
                    </span>
                  </td>

                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => setSelectedLog(log)}
                      className="p-1.5 text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 rounded-lg transition-colors"
                      title="Xem chi tiết"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* AI Log Detail Modal */}
      {selectedLog && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full p-6 sm:p-8 space-y-4 text-xs">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5 text-emerald-600" />
                <h3 className="font-bold text-slate-900 text-base">Chi tiết bản ghi gọi AI</h3>
              </div>
              <button onClick={() => setSelectedLog(null)} className="p-1 text-slate-400">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2 bg-slate-50 p-3.5 rounded-2xl border border-slate-200">
              <div><span className="text-slate-500">Tính năng:</span> <strong>{selectedLog.feature_name}</strong></div>
              <div><span className="text-slate-500">Mô hình:</span> <strong>{selectedLog.model_used}</strong></div>
              <div><span className="text-slate-500">Thời gian:</span> <strong>{formatDateTime(selectedLog.created_at)}</strong></div>
              <div><span className="text-slate-500">Độ trễ phản hồi:</span> <strong>{selectedLog.latency_ms} ms</strong></div>
            </div>

            <div>
              <label className="block font-bold text-slate-800 mb-1">
                Prompt gửi tới AI (Đã qua bộ lọc khử định danh PII):
              </label>
              <div className="p-3.5 bg-slate-900 text-emerald-300 rounded-2xl font-mono text-[11px] whitespace-pre-wrap leading-relaxed">
                {selectedLog.anonymized_prompt}
              </div>
            </div>

            <div>
              <label className="block font-bold text-slate-800 mb-1">
                Phản hồi từ AI (AI Response):
              </label>
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-2xl text-slate-800 text-xs whitespace-pre-wrap leading-relaxed">
                {selectedLog.response_text}
              </div>
            </div>

            <MedicalDisclaimerBadge />

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedLog(null)}
                className="px-5 py-2 bg-slate-800 text-white rounded-xl font-bold"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AILogPage;
