import React, { useState, useEffect } from 'react';
import {
  Users,
  UserPlus,
  Search,
  Shield,
  Stethoscope,
  CreditCard,
  CheckCircle2,
  XCircle,
  X,
  Edit2,
  Lock
} from 'lucide-react';
import api from '../../services/api';
import { useToast } from '../../context/ToastContext';
import { getRoleInfo, formatDate } from '../../utils/formatters';

const UserManagementPage = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);

  const { toastSuccess, toastError } = useToast();

  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    role: 'doctor',
    is_active: true,
  });

  const loadUsers = async () => {
    setLoading(true);
    try {
      const params = {};
      if (roleFilter) params.role = roleFilter;
      if (searchQuery) params.search = searchQuery;
      const response = await api.get('/users', { params });
      setUsers(response.data || []);
    } catch (err) {
      console.error('Failed to load users:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, [roleFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    loadUsers();
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/users', newUser);
      toastSuccess(`Đã tạo tài khoản thành công: ${response.data.username}`);
      setShowAddModal(false);
      setNewUser({
        username: '',
        email: '',
        full_name: '',
        password: '',
        role: 'doctor',
        is_active: true,
      });
      loadUsers();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Tạo tài khoản thất bại');
    }
  };

  const handleToggleStatus = async (user) => {
    try {
      await api.put(`/users/${user.id}`, { is_active: !user.is_active });
      toastSuccess(`Đã ${!user.is_active ? 'kích hoạt' : 'khóa'} tài khoản ${user.username}`);
      loadUsers();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Cập nhật trạng thái thất bại');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Users className="w-6 h-6 text-purple-600" />
            Quản trị tài khoản & Phân quyền RBAC
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Quản lý người dùng, gán vai trò nhân viên và kiểm soát trạng thái hoạt động
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-purple-600 hover:bg-purple-700 text-white rounded-xl text-xs font-bold shadow-md transition-colors self-start sm:self-auto"
        >
          <UserPlus className="w-4 h-4" />
          Thêm người dùng mới
        </button>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-3xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-3">
        <form onSubmit={handleSearch} className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Tìm theo Tên đăng nhập, Họ tên, Email..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </form>

        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          className="px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="">-- Tất cả vai trò --</option>
          <option value="admin">Quản trị viên (Admin)</option>
          <option value="receptionist">Lễ tân (Receptionist)</option>
          <option value="doctor">Bác sĩ (Doctor)</option>
          <option value="accountant">Thu ngân / Kế toán (Accountant)</option>
        </select>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Tên đăng nhập</th>
                <th className="py-3.5 px-4">Họ và tên</th>
                <th className="py-3.5 px-4">Email</th>
                <th className="py-3.5 px-4">Vai trò (Role)</th>
                <th className="py-3.5 px-4">Trạng thái</th>
                <th className="py-3.5 px-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Đang tải danh sách tài khoản...
                  </td>
                </tr>
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Không tìm thấy người dùng nào
                  </td>
                </tr>
              ) : (
                users.map((u) => {
                  const roleInfo = getRoleInfo(u.role);
                  return (
                    <tr key={u.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-slate-900">
                        {u.username}
                      </td>

                      <td className="py-3.5 px-4 font-semibold text-slate-800">
                        {u.full_name}
                      </td>

                      <td className="py-3.5 px-4 text-slate-500">
                        {u.email || '---'}
                      </td>

                      <td className="py-3.5 px-4">
                        <span className={`inline-flex px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${roleInfo.color}`}>
                          {roleInfo.label}
                        </span>
                      </td>

                      <td className="py-3.5 px-4">
                        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          u.is_active
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-amber-100 text-amber-900'
                        }`}>
                          {u.is_active ? 'Hoạt động' : 'Chưa hoạt động'}
                        </span>
                      </td>

                      <td className="py-3.5 px-4 text-right">
                        <button
                          onClick={() => handleToggleStatus(u)}
                          className={`px-3 py-1 rounded-lg text-[11px] font-bold transition-colors ${
                            u.is_active
                              ? 'bg-rose-50 text-rose-700 hover:bg-rose-100'
                              : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                          }`}
                        >
                          {u.is_active ? 'Khóa' : 'Kích hoạt'}
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add User Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-lg w-full p-6 sm:p-8 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-purple-500 text-white rounded-xl">
                  <UserPlus className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-slate-900 text-lg">Tạo tài khoản nhân viên mới</h3>
              </div>
              <button onClick={() => setShowAddModal(false)} className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateUser} className="space-y-4 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Tên đăng nhập *</label>
                <input
                  type="text"
                  required
                  value={newUser.username}
                  onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                  placeholder="dr_lan, ketoan2..."
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Họ và tên đầy đủ *</label>
                <input
                  type="text"
                  required
                  value={newUser.full_name}
                  onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                  placeholder="BS. Vũ Mai Lan"
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Email</label>
                <input
                  type="email"
                  value={newUser.email}
                  onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                  placeholder="lan.vu@phongkham.vn"
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Mật khẩu ban đầu *</label>
                <input
                  type="password"
                  required
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                  placeholder="••••••••"
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Phân quyền vai trò (Role) *</label>
                <select
                  value={newUser.role}
                  onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                  className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-purple-500"
                >
                  <option value="doctor">Bác sĩ (Doctor)</option>
                  <option value="receptionist">Lễ tân (Receptionist)</option>
                  <option value="accountant">Thu ngân / Kế toán (Accountant)</option>
                  <option value="admin">Quản trị viên (Admin)</option>
                </select>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-100 text-slate-700 font-bold rounded-xl"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow transition-colors"
                >
                  Tạo tài khoản
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagementPage;
