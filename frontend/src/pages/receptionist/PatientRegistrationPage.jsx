import React, { useState, useEffect } from 'react';
import {
  Users,
  Search,
  UserPlus,
  Phone,
  CreditCard,
  AlertTriangle,
  FileText,
  Calendar,
  X,
  Check,
  ShieldAlert,
  ChevronRight
} from 'lucide-react';
import { patientService } from '../../services/patientService';
import { useToast } from '../../context/ToastContext';
import { formatDate } from '../../utils/formatters';
import { useNavigate } from 'react-router-dom';

const PatientRegistrationPage = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const { toastSuccess, toastError } = useToast();
  const navigate = useNavigate();

  // New patient form state
  const [formData, setFormData] = useState({
    full_name: '',
    date_of_birth: '1990-01-01',
    gender: 'Nam',
    phone: '',
    identity_card: '',
    insurance_number: '',
    address: '',
    allergies: '',
    medical_history: '',
  });

  const loadPatients = async (query = '') => {
    setLoading(true);
    try {
      const data = await patientService.getPatients(query);
      setPatients(data || []);
    } catch (err) {
      console.error('Failed to load patients:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPatients();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    loadPatients(searchQuery);
  };

  const handleCreatePatient = async (e) => {
    e.preventDefault();
    if (!formData.full_name || !formData.phone) {
      toastError('Vui lòng nhập Họ tên và Số điện thoại');
      return;
    }

    try {
      const created = await patientService.createPatient(formData);
      toastSuccess(`Đã đăng ký thành công bệnh nhân: ${created.full_name} (Mã BN: ${created.medical_code})`);
      setShowAddModal(false);
      setFormData({
        full_name: '',
        date_of_birth: '1990-01-01',
        gender: 'Nam',
        phone: '',
        identity_card: '',
        insurance_number: '',
        address: '',
        allergies: '',
        medical_history: '',
      });
      loadPatients();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Đăng ký bệnh nhân thất bại');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
            Quản lý hồ sơ & Đăng ký bệnh nhân
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Tra cứu lịch sử khám, quản lý mã định danh BN và ghi nhận tiền sử dị ứng
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-medical-600 hover:bg-medical-700 text-white rounded-xl text-xs font-bold shadow-md transition-colors self-start sm:self-auto"
        >
          <UserPlus className="w-4 h-4" />
          Tiếp nhận bệnh nhân mới
        </button>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Tìm kiếm theo Tên, Số điện thoại, Mã BN (BN-YYYYMMDD-XXXX), CCCD hoặc Số thẻ BHYT..."
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-medical-500 shadow-2xs"
          />
        </div>
        <button
          type="submit"
          className="px-5 py-2.5 bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold rounded-xl transition-colors"
        >
          Tìm kiếm
        </button>
      </form>

      {/* Patient Cards / Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Mã BN / Ngày tạo</th>
                <th className="py-3.5 px-4">Họ và tên & Giới tính</th>
                <th className="py-3.5 px-4">Liên hệ & CCCD</th>
                <th className="py-3.5 px-4">BHYT</th>
                <th className="py-3.5 px-4">Cảnh báo dị ứng</th>
                <th className="py-3.5 px-4 text-right">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Đang tải danh sách hồ sơ bệnh nhân...
                  </td>
                </tr>
              ) : patients.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Không tìm thấy bệnh nhân nào
                  </td>
                </tr>
              ) : (
                patients.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-mono">
                      <span className="font-bold text-medical-700">{p.medical_code}</span>
                      <div className="text-[11px] text-slate-400">{formatDate(p.created_at)}</div>
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="font-bold text-slate-900">{p.full_name}</div>
                      <div className="text-[11px] text-slate-500">
                        {p.gender} • Sinh ngày: {formatDate(p.date_of_birth)}
                      </div>
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-1 text-slate-800 font-medium">
                        <Phone className="w-3 h-3 text-slate-400" />
                        {p.phone}
                      </div>
                      <div className="text-[11px] text-slate-500">CCCD: {p.identity_card || 'Chưa cập nhật'}</div>
                    </td>

                    <td className="py-3.5 px-4">
                      {p.insurance_number ? (
                        <span className="px-2 py-0.5 bg-sky-50 text-sky-800 border border-sky-200 rounded font-mono text-[11px]">
                          {p.insurance_number}
                        </span>
                      ) : (
                        <span className="text-slate-400 italic text-[11px]">Không có BHYT</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4">
                      {p.allergies ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 bg-rose-50 text-rose-800 border border-rose-200 rounded-full font-bold text-[10px]">
                          <AlertTriangle className="w-3 h-3 text-rose-600" />
                          {p.allergies}
                        </span>
                      ) : (
                        <span className="text-emerald-700 font-medium text-[11px]">Không có</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => setSelectedPatient(p)}
                          className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-semibold text-[11px] transition-colors"
                        >
                          Chi tiết
                        </button>
                        <button
                          onClick={() => navigate(`/receptionist/appointments?patient_id=${p.id}`)}
                          className="px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-lg font-semibold text-[11px] transition-colors"
                        >
                          Đặt lịch
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Patient Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full p-6 sm:p-8 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-medical-500 text-white rounded-xl">
                  <UserPlus className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">Đăng ký tiếp nhận bệnh nhân mới</h3>
                  <p className="text-xs text-slate-500">Mã bệnh nhân (BN-YYYYMMDD-XXXX) sẽ được tạo tự động</p>
                </div>
              </div>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-2 text-slate-400 hover:text-slate-600 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreatePatient} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Họ và tên bệnh nhân *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                    placeholder="Nguyễn Văn A"
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Số điện thoại *
                  </label>
                  <input
                    type="tel"
                    required
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    placeholder="0912345678"
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Ngày sinh
                  </label>
                  <input
                    type="date"
                    value={formData.date_of_birth}
                    onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Giới tính
                  </label>
                  <select
                    value={formData.gender}
                    onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  >
                    <option value="Nam">Nam</option>
                    <option value="Nữ">Nữ</option>
                    <option value="Khác">Khác</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Số CCCD / CMND (12 số)
                  </label>
                  <input
                    type="text"
                    value={formData.identity_card}
                    onChange={(e) => setFormData({ ...formData, identity_card: e.target.value })}
                    placeholder="001202001234"
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Mã thẻ BHYT (15 ký tự)
                  </label>
                  <input
                    type="text"
                    value={formData.insurance_number}
                    onChange={(e) => setFormData({ ...formData, insurance_number: e.target.value.toUpperCase() })}
                    placeholder="DN4010123456789"
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-mono focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Địa chỉ thường trú
                  </label>
                  <input
                    type="text"
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    placeholder="Phường Quang Trung, TP. Thái Nguyên, Thái Nguyên"
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block text-xs font-bold text-rose-700 mb-1 flex items-center gap-1">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    Tiền sử dị ứng thuốc (Nếu có)
                  </label>
                  <input
                    type="text"
                    value={formData.allergies}
                    onChange={(e) => setFormData({ ...formData, allergies: e.target.value })}
                    placeholder="Ví dụ: Dị ứng Penicillin, Aspirin, phấn hoa..."
                    className="w-full px-3.5 py-2 bg-rose-50/50 border border-rose-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-rose-500"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Tiền sử bệnh án / Bệnh nền
                  </label>
                  <textarea
                    rows={2}
                    value={formData.medical_history}
                    onChange={(e) => setFormData({ ...formData, medical_history: e.target.value })}
                    placeholder="Ví dụ: Tăng huyết áp, Đái tháo đường type 2..."
                    className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:ring-2 focus:ring-medical-500"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 bg-medical-600 hover:bg-medical-700 text-white text-xs font-bold rounded-xl shadow-md transition-colors"
                >
                  Tạo hồ sơ bệnh nhân
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Patient Detail Drawer/Modal */}
      {selectedPatient && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-lg w-full p-6 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div>
                <h3 className="font-bold text-slate-900 text-lg">{selectedPatient.full_name}</h3>
                <p className="text-xs font-mono font-bold text-medical-700">Mã BN: {selectedPatient.medical_code}</p>
              </div>
              <button
                onClick={() => setSelectedPatient(null)}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2 bg-slate-50 p-4 rounded-2xl border border-slate-200">
                <div><span className="text-slate-500">Ngày sinh:</span> <strong>{formatDate(selectedPatient.date_of_birth)}</strong></div>
                <div><span className="text-slate-500">Giới tính:</span> <strong>{selectedPatient.gender}</strong></div>
                <div><span className="text-slate-500">Điện thoại:</span> <strong>{selectedPatient.phone}</strong></div>
                <div><span className="text-slate-500">CCCD:</span> <strong>{selectedPatient.identity_card || '---'}</strong></div>
                <div className="col-span-2"><span className="text-slate-500">BHYT:</span> <strong className="font-mono">{selectedPatient.insurance_number || 'Không'}</strong></div>
                <div className="col-span-2"><span className="text-slate-500">Địa chỉ:</span> <span>{selectedPatient.address || 'Việt Nam'}</span></div>
              </div>

              {selectedPatient.allergies && (
                <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-900">
                  <div className="font-bold flex items-center gap-1.5 mb-1">
                    <AlertTriangle className="w-4 h-4 text-rose-600" />
                    Cảnh báo dị ứng:
                  </div>
                  <p>{selectedPatient.allergies}</p>
                </div>
              )}

              {selectedPatient.medical_history && (
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-700">
                  <div className="font-bold mb-1">Tiền sử bệnh lý:</div>
                  <p>{selectedPatient.medical_history}</p>
                </div>
              )}
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
              <button
                onClick={() => setSelectedPatient(null)}
                className="px-4 py-2 bg-slate-100 text-slate-700 text-xs font-bold rounded-xl"
              >
                Đóng
              </button>
              <button
                onClick={() => {
                  const pid = selectedPatient.id;
                  setSelectedPatient(null);
                  navigate(`/receptionist/appointments?patient_id=${pid}`);
                }}
                className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow transition-colors"
              >
                Đặt lịch khám cho bệnh nhân
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientRegistrationPage;
