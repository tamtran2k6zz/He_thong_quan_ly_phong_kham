import React, { useState, useEffect } from 'react';
import {
  Pill,
  Plus,
  Search,
  AlertTriangle,
  PackagePlus,
  CheckCircle2,
  X,
  RefreshCw
} from 'lucide-react';
import { consultationService } from '../../services/consultationService';
import { useToast } from '../../context/ToastContext';
import { formatCurrency } from '../../utils/formatters';

const MedicineCatalogPage = () => {
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [replenishModal, setReplenishModal] = useState(null);
  const [addQty, setAddQty] = useState(50);

  const { toastSuccess, toastError } = useToast();

  const [newMed, setNewMed] = useState({
    name: '',
    code: '',
    active_ingredient: '',
    dosage_form: 'Viên nén',
    unit_price: 2000,
    stock_quantity: 100,
    usage_instructions: 'Uống sau bữa ăn',
    is_active: true,
  });

  const loadMedicines = async (query = '') => {
    setLoading(true);
    try {
      const data = await consultationService.getMedicines(query, null);
      setMedicines(data || []);
    } catch (err) {
      console.error('Failed to load medicines:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMedicines();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    loadMedicines(searchTerm);
  };

  const handleCreateMedicine = async (e) => {
    e.preventDefault();
    try {
      await consultationService.createMedicine(newMed);
      toastSuccess(`Đã thêm thuốc ${newMed.name} vào danh mục`);
      setShowAddModal(false);
      setNewMed({
        name: '',
        code: '',
        active_ingredient: '',
        dosage_form: 'Viên nén',
        unit_price: 2000,
        stock_quantity: 100,
        usage_instructions: 'Uống sau bữa ăn',
        is_active: true,
      });
      loadMedicines();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Thêm thuốc thất bại');
    }
  };

  const handleReplenishStock = async () => {
    if (!replenishModal) return;
    try {
      const newStock = replenishModal.stock_quantity + parseInt(addQty);
      await consultationService.updateMedicine(replenishModal.id, {
        stock_quantity: newStock,
      });
      toastSuccess(`Đã nhập thêm ${addQty} đơn vị thuốc ${replenishModal.name}`);
      setReplenishModal(null);
      loadMedicines();
    } catch (err) {
      toastError(err.response?.data?.detail || 'Nhập kho thất bại');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Pill className="w-6 h-6 text-emerald-600" />
            Danh mục & Kho dược phẩm phòng khám
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Theo dõi lượng tồn kho, hoạt chất biệt dược, đơn giá và bổ sung nhập kho
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow-md transition-colors self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          Thêm thuốc mới
        </button>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Tìm theo tên thuốc, hoạt chất, mã thuốc..."
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <button type="submit" className="px-5 py-2.5 bg-slate-800 text-white rounded-xl text-xs font-semibold">
          Tìm kiếm
        </button>
      </form>

      {/* Medicines Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 uppercase font-semibold border-b border-slate-200 text-[11px]">
              <tr>
                <th className="py-3.5 px-4">Mã thuốc</th>
                <th className="py-3.5 px-4">Tên thuốc & Dạng bào chế</th>
                <th className="py-3.5 px-4">Hoạt chất chính</th>
                <th className="py-3.5 px-4">Đơn giá</th>
                <th className="py-3.5 px-4">Tồn kho</th>
                <th className="py-3.5 px-4 text-right">Nhập kho</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Đang tải danh mục thuốc...
                  </td>
                </tr>
              ) : medicines.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-400 italic">
                    Không tìm thấy thuốc nào
                  </td>
                </tr>
              ) : (
                medicines.map((m) => {
                  const isLow = m.stock_quantity < 20;
                  return (
                    <tr key={m.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3.5 px-4 font-mono font-bold text-slate-700">
                        {m.code}
                      </td>

                      <td className="py-3.5 px-4">
                        <div className="font-bold text-slate-900">{m.name}</div>
                        <div className="text-[11px] text-slate-500">{m.dosage_form || 'Viên nén'}</div>
                      </td>

                      <td className="py-3.5 px-4 text-slate-700 font-medium">
                        {m.active_ingredient || '---'}
                      </td>

                      <td className="py-3.5 px-4 font-bold text-emerald-800 font-mono">
                        {formatCurrency(m.unit_price)}
                      </td>

                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-1.5">
                          <span className={`font-extrabold font-mono text-sm ${isLow ? 'text-rose-600' : 'text-slate-800'}`}>
                            {m.stock_quantity}
                          </span>
                          {isLow && (
                            <span className="px-2 py-0.5 bg-rose-100 text-rose-800 text-[10px] font-bold rounded-full flex items-center gap-1">
                              <AlertTriangle className="w-3 h-3" /> Sắp hết
                            </span>
                          )}
                        </div>
                      </td>

                      <td className="py-3.5 px-4 text-right">
                        <button
                          onClick={() => setReplenishModal(m)}
                          className="inline-flex items-center gap-1 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-bold transition-colors"
                        >
                          <PackagePlus className="w-3.5 h-3.5" />
                          Nhập thêm
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

      {/* Replenish Stock Modal */}
      {replenishModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-base">Nhập thêm kho thuốc</h3>
              <button onClick={() => setReplenishModal(null)} className="p-1 text-slate-400">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-3 bg-slate-50 rounded-2xl">
              <div className="font-bold text-slate-900 text-sm">{replenishModal.name}</div>
              <div className="text-slate-500">Tồn kho hiện tại: <strong className="font-mono">{replenishModal.stock_quantity}</strong></div>
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">Số lượng nhập thêm:</label>
              <input
                type="number"
                min="1"
                value={addQty}
                onChange={(e) => setAddQty(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-bold font-mono text-center text-sm"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setReplenishModal(null)}
                className="px-4 py-2 bg-slate-100 rounded-xl font-bold"
              >
                Hủy
              </button>
              <button
                onClick={handleReplenishStock}
                className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold"
              >
                Xác nhận nhập kho
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Medicine Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl max-w-lg w-full p-6 sm:p-8 space-y-4 text-xs">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-base">Thêm thuốc mới vào danh mục</h3>
              <button onClick={() => setShowAddModal(false)} className="p-1 text-slate-400">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateMedicine} className="space-y-3">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Tên thuốc biệt dược *</label>
                <input
                  type="text"
                  required
                  value={newMed.name}
                  onChange={(e) => setNewMed({ ...newMed, name: e.target.value })}
                  placeholder="Paracetamol 500mg"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Hoạt chất chính *</label>
                <input
                  type="text"
                  required
                  value={newMed.active_ingredient}
                  onChange={(e) => setNewMed({ ...newMed, active_ingredient: e.target.value })}
                  placeholder="Acetaminophen"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Dạng bào chế</label>
                  <input
                    type="text"
                    value={newMed.dosage_form}
                    onChange={(e) => setNewMed({ ...newMed, dosage_form: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Đơn giá (VNĐ) *</label>
                  <input
                    type="number"
                    value={newMed.unit_price}
                    onChange={(e) => setNewMed({ ...newMed, unit_price: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Số lượng ban đầu</label>
                <input
                  type="number"
                  value={newMed.stock_quantity}
                  onChange={(e) => setNewMed({ ...newMed, stock_quantity: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-mono"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-100 rounded-xl font-bold"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold shadow"
                >
                  Lưu vào danh mục
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicineCatalogPage;
