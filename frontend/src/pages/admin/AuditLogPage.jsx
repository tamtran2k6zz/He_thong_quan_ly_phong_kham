import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Search,
  Filter,
  Clock,
  User,
  Activity,
  Globe,
  RefreshCw
} from 'lucide-react';
import { auditService } from '../../services/auditService';
import { formatDateTime } from '../../utils/formatters';

const AuditLogPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionFilter, setActionFilter] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const loadLogs = async () => {
    setLoading(true);
    try {
      const params = { limit: 100 };
      if (actionFilter) params.action = actionFilter;
      const data = await auditService.getAuditLogs(params);
      setLogs(data || []);
    } catch (err) {
      console.error('Failed to load audit logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [actionFilter]);

  const filteredLogs = logs.filter((log) => {
    if (!searchTerm) return true;
    const q = searchTerm.toLowerCase();
    return (
      log.action?.toLowerCase().includes(q) ||
      log.resource_type?.toLowerCase().includes(q) ||
      log.details?.toLowerCase().includes(q) ||
      log.ip_address?.includes(q)
    );
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-purple-600" />
            Nhật ký kiểm toán & Giám sát hệ thống (Audit Trail)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Ghi vết toàn bộ hành vi truy cập, xem sửa bệnh án, kê đơn và giao dịch tài chính
          </p>
        </div>

        <button
          onClick={loadLogs}
          className="flex items-center gap-1.5 px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-bold shadow-2xs transition-colors self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Làm mới nhật ký
        </button>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-3xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Tìm theo chi tiết, IP, hành động..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <select
          value={actionFilter}
          onChange={(e) => setActionFilter(e.target.value)}
          className="px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:ring-2 focus:ring-purple-500"
        >
          <option value="">-- Tất cả hành vi --</option>
          <option value="LOGIN">LOGIN (Đăng nhập)</option>
          <option value="VIEW_PATIENT">VIEW_PATIENT (Xem hồ sơ bệnh nhân)</option>
          <option value="BOOK_APPOINTMENT">BOOK_APPOINTMENT (Đặt lịch khám)</option>
          <option value="CHECKIN_APPOINTMENT">CHECKIN_APPOINTMENT (Tiếp đón)</option>
          <option value="CREATE_MEDICAL_RECORD">CREATE_MEDICAL_RECORD (Khám bệnh)</option>
          <option value="COMPLETE_MEDICAL_RECORD">COMPLETE_MEDICAL_RECORD (Hoàn tất khám)</option>
        </select>
      </div>

      {/* Audit Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Thời gian</th>
                <th className="py-3.5 px-4">Người thực hiện</th>
                <th className="py-3.5 px-4">Hành vi (Action)</th>
                <th className="py-3.5 px-4">Đối tượng</th>
                <th className="py-3.5 px-4">Địa chỉ IP</th>
                <th className="py-3.5 px-4">Chi tiết thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Đang tải nhật ký kiểm toán...
                  </td>
                </tr>
              ) : filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Không có bản ghi nhật ký nào
                  </td>
                </tr>
              ) : (
                filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-mono text-slate-500 whitespace-nowrap">
                      {formatDateTime(log.created_at)}
                    </td>

                    <td className="py-3.5 px-4">
                      <span className="font-bold text-slate-800">
                        {log.user?.full_name || log.user?.username || `User #${log.user_id || 'System'}`}
                      </span>
                    </td>

                    <td className="py-3.5 px-4">
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono bg-purple-50 text-purple-800 border border-purple-200">
                        {log.action}
                      </span>
                    </td>

                    <td className="py-3.5 px-4 font-semibold text-slate-700">
                      {log.resource_type} {log.resource_id ? `#${log.resource_id}` : ''}
                    </td>

                    <td className="py-3.5 px-4 font-mono text-slate-500 text-[11px]">
                      {log.ip_address || '127.0.0.1'}
                    </td>

                    <td className="py-3.5 px-4 text-slate-600 max-w-md">
                      {log.details || '---'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AuditLogPage;
