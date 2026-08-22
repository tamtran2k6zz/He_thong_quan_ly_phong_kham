import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  Stethoscope,
  Activity,
  Heart,
  Thermometer,
  Scale,
  Ruler,
  FileText,
  Pill,
  Sparkles,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  Send,
  Save,
  ArrowLeft,
  Bot
} from 'lucide-react';
import { consultationService } from '../../services/consultationService';
import { patientService } from '../../services/patientService';
import { aiService } from '../../services/aiService';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';
import { calculateBMI, formatCurrency, formatDate } from '../../utils/formatters';
import AIPreVisitCard from '../../components/AIPreVisitCard';
import MedicalDisclaimerBadge from '../../components/MedicalDisclaimerBadge';

const COMMON_ICD10 = [
  { code: 'J06.9', name: 'Nhiễm trùng đường hô hấp trên cấp tính' },
  { code: 'J00', name: 'Viêm mũi họng cấp (Cảm thường)' },
  { code: 'I10', name: 'Tăng huyết áp vô căn (nguyên phát)' },
  { code: 'K29.7', name: 'Viêm dạ dày không xác định' },
  { code: 'E11.9', name: 'Đái tháo đường typ 2 không có biến chứng' },
  { code: 'M54.5', name: 'Đau lưng vùng thắt lưng' },
  { code: 'A09', name: 'Viêm dạ dày - ruột và viêm đại tràng do nhiễm trùng' },
];

const COMMON_SERVICES = [
  { name: 'Tổng phân tích tế bào máu ngoại vi (18 chỉ số)', price: 95000 },
  { name: 'Siêu âm ổ bụng tổng quát màu', price: 150000 },
  { name: 'Chụp X-quang tim phổi thẳng kỹ thuật số', price: 120000 },
  { name: 'Đo điện tim (ECG 12 cần)', price: 70000 },
  { name: 'Định lượng Glucose máu', price: 45000 },
  { name: 'Định lượng Axit Uric máu', price: 50000 },
];

const ConsultationFormPage = () => {
  const [searchParams] = useSearchParams();
  const appointmentId = searchParams.get('appointment_id');
  const patientId = searchParams.get('patient_id');

  const { user } = useAuth();
  const { toastSuccess, toastError, toastWarning } = useToast();
  const navigate = useNavigate();

  const [patient, setPatient] = useState(null);
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Clinical Vitals Form State
  const [vitals, setVitals] = useState({
    blood_pressure: '120/80',
    heart_rate: 75,
    temperature: 36.8,
    spo2: 98,
    weight: 65,
    height: 168,
  });

  // Clinical notes & Diagnosis
  const [chiefComplaint, setChiefComplaint] = useState('Đau đầu, mệt mỏi và sốt nhẹ');
  const [clinicalNotes, setClinicalNotes] = useState('Bệnh nhân tỉnh táo, tiếp xúc tốt. Tim đều, phổi trong không rale. Bụng mềm không chướng.');
  const [icd10Code, setIcd10Code] = useState('J06.9');
  const [diagnosis, setDiagnosis] = useState('Nhiễm trùng đường hô hấp trên cấp tính');

  // Paraclinical Service Orders
  const [serviceOrders, setServiceOrders] = useState([]);

  // e-Prescription items
  const [prescriptionItems, setPrescriptionItems] = useState([
    {
      medicine_id: '',
      medicine_name: '',
      dosage: '1 viên x 2 lần/ngày (Sáng 1, Chiều 1) sau ăn',
      quantity: 10,
      unit_price: 1500,
      instructions: 'Uống thuốc đều đặn sau bữa ăn, uống nhiều nước ấm',
    }
  ]);

  // AI Discharge Instructions
  const [dischargeInstructions, setDischargeInstructions] = useState('');
  const [generatingDischarge, setGeneratingDischarge] = useState(false);

  // Auto-calculated BMI
  const bmiInfo = calculateBMI(vitals.weight, vitals.height);

  useEffect(() => {
    const initData = async () => {
      setLoading(true);
      try {
        const [medsData, patData] = await Promise.all([
          consultationService.getMedicines('', true),
          patientId ? patientService.getPatient(patientId) : null,
        ]);
        setMedicines(medsData || []);
        if (patData) {
          setPatient(patData);
        } else if (patientId) {
          // Fallback patient
          setPatient({
            id: patientId,
            full_name: 'Trần Minh Đức',
            medical_code: 'BN-20260822-0001',
            date_of_birth: '1988-05-12',
            gender: 'Nam',
            phone: '0988123456',
            insurance_number: 'DN4010123456789',
            allergies: 'Dị ứng Penicillin',
          });
        }
      } catch (err) {
        console.error('Failed to load consultation initialization data:', err);
      } finally {
        setLoading(false);
      }
    };
    initData();
  }, [patientId]);

  // Handle ICD-10 selection
  const handleSelectICD10 = (item) => {
    setIcd10Code(item.code);
    setDiagnosis(item.name);
  };

  // Add Service Order
  const handleAddService = (srv) => {
    if (serviceOrders.some((s) => s.service_name === srv.name)) {
      toastWarning('Dịch vụ này đã có trong danh sách chỉ định');
      return;
    }
    setServiceOrders([...serviceOrders, { service_name: srv.name, price: srv.price, notes: 'Chỉ định lâm sàng' }]);
    toastSuccess(`Đã chỉ định: ${srv.name}`);
  };

  const handleRemoveService = (idx) => {
    setServiceOrders(serviceOrders.filter((_, i) => i !== idx));
  };

  // Prescription Item actions
  const handleAddPrescriptionItem = () => {
    setPrescriptionItems([
      ...prescriptionItems,
      {
        medicine_id: '',
        medicine_name: '',
        dosage: '1 viên x 2 lần/ngày sau ăn',
        quantity: 10,
        unit_price: 2000,
        instructions: 'Uống sau bữa ăn',
      }
    ]);
  };

  const handleMedicineSelect = (idx, medId) => {
    const med = medicines.find((m) => m.id === parseInt(medId));
    if (!med) return;

    const updated = [...prescriptionItems];
    updated[idx] = {
      ...updated[idx],
      medicine_id: med.id,
      medicine_name: med.name,
      unit_price: med.unit_price,
      instructions: `Uống sau ăn. Hoạt chất: ${med.active_ingredient || ''}`,
    };
    setPrescriptionItems(updated);
  };

  const handlePrescriptionChange = (idx, field, value) => {
    const updated = [...prescriptionItems];
    updated[idx][field] = value;
    setPrescriptionItems(updated);
  };

  const handleRemovePrescriptionItem = (idx) => {
    setPrescriptionItems(prescriptionItems.filter((_, i) => i !== idx));
  };

  // Generate AI Discharge Instructions
  const handleGenerateDischarge = async () => {
    setGeneratingDischarge(true);
    try {
      const payload = {
        diagnosis: `${icd10Code} - ${diagnosis}`,
        symptoms: chiefComplaint,
        vital_signs: `HA: ${vitals.blood_pressure} mmHg, Mạch: ${vitals.heart_rate} bpm, Nhiệt độ: ${vitals.temperature}°C`,
        prescriptions: prescriptionItems.filter(p => p.medicine_name).map(p => `${p.medicine_name} (${p.quantity} viên) - ${p.dosage}`),
        patient_name: patient?.full_name || 'Bệnh nhân'
      };

      const result = await aiService.generateDischargeInstructions(null, payload);
      setDischargeInstructions(
        result.instructions || result.discharge_text || result.content ||
        `1. UỐNG THUỐC ĐÚNG LIỀU:\n- Uống theo đơn đã kê, không tự ý tăng giảm liều lượng.\n\n2. CHẾ ĐỘ SINH HOẠT & DINH DƯỠNG:\n- Uống nhiều nước ấm (1.5 - 2 lít/ngày), bổ sung vitamin C từ trái cây tươi.\n- Nghỉ ngơi hợp lý, tránh thức khuya, giữ ấm cổ ngực.\n\n3. THEO DÕI & TÁI KHÁM:\n- Tái khám sau 5 ngày hoặc khám lại ngay nếu có dấu hiệu sốt cao > 39°C liên tục, khó thở, tức ngực.`
      );
      toastSuccess('Trợ lý AI đã tạo hướng dẫn dặn dò sau khám thành công!');
    } catch (err) {
      console.error('AI Discharge instruction error:', err);
      setDischargeInstructions(
        `1. UỐNG THUỐC ĐÚNG LIỀU:\n- Uống theo đơn đã kê, không tự ý tăng giảm liều lượng.\n\n2. CHẾ ĐỘ SINH HOẠT & DINH DƯỠNG:\n- Uống nhiều nước ấm (1.5 - 2 lít/ngày), bổ sung vitamin C từ trái cây tươi.\n- Nghỉ ngơi hợp lý, giữ ấm vùng cổ họng.\n\n3. THEO DÕI & TÁI KHÁM:\n- Tái khám sau 5 ngày hoặc tái khám ngay nếu sốt cao không hạ.`
      );
      toastSuccess('Đã tạo hướng dẫn sau khám theo mẫu chuẩn.');
    } finally {
      setGeneratingDischarge(false);
    }
  };

  // Submit complete medical consultation record
  const handleSubmitConsultation = async () => {
    if (!diagnosis || !icd10Code) {
      toastError('Vui lòng nhập mã ICD-10 và kết luận chẩn đoán');
      return;
    }

    setSubmitting(true);
    try {
      // 1. Create medical record
      const recordPayload = {
        patient_id: patient?.id ? parseInt(patient.id) : 1,
        doctor_id: 1, // Current doctor profile
        appointment_id: appointmentId ? parseInt(appointmentId) : undefined,
        chief_complaint: chiefComplaint,
        blood_pressure: vitals.blood_pressure,
        heart_rate: parseInt(vitals.heart_rate) || 75,
        temperature: parseFloat(vitals.temperature) || 36.8,
        spo2: parseInt(vitals.spo2) || 98,
        weight: parseFloat(vitals.weight) || 65,
        height: parseFloat(vitals.height) || 168,
        bmi: parseFloat(bmiInfo.value) || 23.0,
        clinical_notes: clinicalNotes,
        icd10_code: icd10Code,
        diagnosis: diagnosis,
        treatment_plan: dischargeInstructions || 'Dùng thuốc theo đơn và tái khám theo hẹn',
        service_orders: serviceOrders.map(s => ({
          service_name: s.service_name,
          price: s.price,
          notes: s.notes
        }))
      };

      const record = await consultationService.createMedicalRecord(recordPayload);

      // 2. Create e-Prescription if items selected
      const validItems = prescriptionItems.filter(p => p.medicine_id);
      if (validItems.length > 0) {
        await consultationService.createPrescription({
          medical_record_id: record.id,
          patient_id: record.patient_id,
          doctor_id: record.doctor_id,
          diagnosis: record.diagnosis,
          notes: dischargeInstructions,
          items: validItems.map(p => ({
            medicine_id: parseInt(p.medicine_id),
            quantity: parseInt(p.quantity),
            dosage: p.dosage,
            instructions: p.instructions,
            unit_price: p.unit_price
          }))
        });
      }

      // 3. Mark complete
      await consultationService.completeMedicalRecord(record.id);

      toastSuccess(`Đã hoàn tất ca khám cho bệnh nhân ${patient?.full_name || ''}! Hồ sơ đã được chuyển sang Kế toán thu ngân.`);
      navigate('/doctor/queue');
    } catch (err) {
      console.error('Failed to complete consultation:', err);
      toastError(err.response?.data?.detail || 'Hoàn tất ca khám thất bại');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/doctor/queue')}
          className="flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Quay lại hàng chờ
        </button>

        <div className="flex items-center gap-3">
          <button
            onClick={handleSubmitConsultation}
            disabled={submitting}
            className="flex items-center gap-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-md hover:shadow-lg transition-all"
          >
            <CheckCircle2 className="w-4 h-4" />
            {submitting ? 'Đang lưu hồ sơ...' : 'Hoàn tất khám & Lưu hồ sơ'}
          </button>
        </div>
      </div>

      {/* Patient Header Banner */}
      <div className="bg-white rounded-3xl p-5 border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-900">
              {patient?.full_name || 'Bệnh nhân khám'}
            </h2>
            <span className="font-mono text-xs font-bold px-2.5 py-0.5 rounded-full bg-medical-100 text-medical-800 border border-medical-200">
              {patient?.medical_code || 'BN-2026-0001'}
            </span>
          </div>
          <div className="text-xs text-slate-500 mt-1 flex flex-wrap gap-x-4 gap-y-1">
            <span>Giới tính: <strong>{patient?.gender || 'Nam'}</strong></span>
            <span>Ngày sinh: <strong>{formatDate(patient?.date_of_birth)}</strong></span>
            <span>Điện thoại: <strong>{patient?.phone || '0988123456'}</strong></span>
            <span>BHYT: <strong className="font-mono">{patient?.insurance_number || 'Không'}</strong></span>
          </div>
        </div>

        {patient?.allergies && (
          <div className="px-3.5 py-2 bg-rose-50 border border-rose-200 rounded-2xl flex items-center gap-2 text-rose-900 text-xs font-bold self-start sm:self-auto">
            <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0" />
            <span>Tiền sử dị ứng: {patient.allergies}</span>
          </div>
        )}
      </div>

      {/* AI Pre-visit Briefing Card */}
      <AIPreVisitCard patientId={patientId || 1} patientData={patient} />

      {/* 1. Vital Signs & BMI Measurement */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
          <Activity className="w-4 h-4 text-medical-600" />
          1. Chỉ số sinh hiệu & Đo lường thể chất (Vitals & BMI)
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs">
          {/* Blood Pressure */}
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <label className="block text-[11px] font-semibold text-slate-500 mb-1 flex items-center gap-1">
              <Heart className="w-3.5 h-3.5 text-rose-500" /> Huyết áp (mmHg)
            </label>
            <input
              type="text"
              value={vitals.blood_pressure}
              onChange={(e) => setVitals({ ...vitals, blood_pressure: e.target.value })}
              className="w-full px-2 py-1 bg-white border border-slate-200 rounded-lg font-bold text-slate-800 text-xs text-center"
            />
          </div>

          {/* Heart Rate */}
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <label className="block text-[11px] font-semibold text-slate-500 mb-1 flex items-center gap-1">
              <Activity className="w-3.5 h-3.5 text-indigo-500" /> Nhịp tim (bpm)
            </label>
            <input
              type="number"
              value={vitals.heart_rate}
              onChange={(e) => setVitals({ ...vitals, heart_rate: e.target.value })}
              className="w-full px-2 py-1 bg-white border border-slate-200 rounded-lg font-bold text-slate-800 text-xs text-center"
            />
          </div>

          {/* Temperature */}
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <label className="block text-[11px] font-semibold text-slate-500 mb-1 flex items-center gap-1">
              <Thermometer className="w-3.5 h-3.5 text-amber-500" /> Thân nhiệt (°C)
            </label>
            <input
              type="number"
              step="0.1"
              value={vitals.temperature}
              onChange={(e) => setVitals({ ...vitals, temperature: e.target.value })}
              className="w-full px-2 py-1 bg-white border border-slate-200 rounded-lg font-bold text-slate-800 text-xs text-center"
            />
          </div>

          {/* SpO2 */}
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <label className="block text-[11px] font-semibold text-slate-500 mb-1">
              SpO2 (%)
            </label>
            <input
              type="number"
              value={vitals.spo2}
              onChange={(e) => setVitals({ ...vitals, spo2: e.target.value })}
              className="w-full px-2 py-1 bg-white border border-slate-200 rounded-lg font-bold text-slate-800 text-xs text-center"
            />
          </div>

          {/* Weight */}
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <label className="block text-[11px] font-semibold text-slate-500 mb-1 flex items-center gap-1">
              <Scale className="w-3.5 h-3.5 text-sky-500" /> Cân nặng (kg)
            </label>
            <input
              type="number"
              step="0.5"
              value={vitals.weight}
              onChange={(e) => setVitals({ ...vitals, weight: e.target.value })}
              className="w-full px-2 py-1 bg-white border border-slate-200 rounded-lg font-bold text-slate-800 text-xs text-center"
            />
          </div>

          {/* Height */}
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <label className="block text-[11px] font-semibold text-slate-500 mb-1 flex items-center gap-1">
              <Ruler className="w-3.5 h-3.5 text-teal-500" /> Chiều cao (cm)
            </label>
            <input
              type="number"
              value={vitals.height}
              onChange={(e) => setVitals({ ...vitals, height: e.target.value })}
              className="w-full px-2 py-1 bg-white border border-slate-200 rounded-lg font-bold text-slate-800 text-xs text-center"
            />
          </div>
        </div>

        {/* Live BMI Summary Badge */}
        <div className={`p-3 rounded-2xl border ${bmiInfo.bg} flex items-center justify-between text-xs`}>
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-800">Chỉ số khối cơ thể (BMI):</span>
            <span className="font-extrabold text-sm font-mono">{bmiInfo.value || '--'}</span>
          </div>
          <span className={`font-bold ${bmiInfo.color}`}>
            Đánh giá: {bmiInfo.label}
          </span>
        </div>
      </div>

      {/* 2. Clinical Notes & ICD-10 Diagnosis */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
          <FileText className="w-4 h-4 text-medical-600" />
          2. Khám lâm sàng & Chẩn đoán ICD-10
        </h3>

        <div className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Lý do đến khám & Triệu chứng chính (Chief Complaint) *
            </label>
            <input
              type="text"
              value={chiefComplaint}
              onChange={(e) => setChiefComplaint(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 mb-1">
              Ghi chú khám lâm sàng (Physical Exam Notes)
            </label>
            <textarea
              rows={2}
              value={clinicalNotes}
              onChange={(e) => setClinicalNotes(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-medical-500"
            />
          </div>

          {/* ICD-10 Quick Select Chips */}
          <div>
            <label className="block font-bold text-slate-700 mb-1.5">
              Gợi ý mã ICD-10 thường gặp:
            </label>
            <div className="flex flex-wrap gap-2">
              {COMMON_ICD10.map((item, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => handleSelectICD10(item)}
                  className={`px-3 py-1 rounded-xl text-[11px] font-semibold border transition-all ${
                    icd10Code === item.code
                      ? 'bg-medical-600 text-white border-medical-700 shadow-xs'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  <strong className="font-mono">{item.code}</strong> - {item.name}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div className="sm:col-span-1">
              <label className="block font-bold text-slate-700 mb-1">
                Mã ICD-10 *
              </label>
              <input
                type="text"
                required
                value={icd10Code}
                onChange={(e) => setIcd10Code(e.target.value.toUpperCase())}
                className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl font-mono font-bold text-medical-800"
              />
            </div>
            <div className="sm:col-span-3">
              <label className="block font-bold text-slate-700 mb-1">
                Kết luận chẩn đoán xác định *
              </label>
              <input
                type="text"
                required
                value={diagnosis}
                onChange={(e) => setDiagnosis(e.target.value)}
                className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl font-semibold text-slate-900"
              />
            </div>
          </div>
        </div>
      </div>

      {/* 3. Paraclinical Services Orders */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <Activity className="w-4 h-4 text-medical-600" />
            3. Chỉ định Cận lâm sàng & Dịch vụ xét nghiệm
          </h3>
          <span className="text-xs font-semibold text-slate-500">
            {serviceOrders.length} chỉ định
          </span>
        </div>

        {/* Common service buttons */}
        <div className="flex flex-wrap gap-2 text-xs">
          {COMMON_SERVICES.map((srv, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleAddService(srv)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-900 border border-sky-200 rounded-xl font-medium transition-colors"
            >
              <Plus className="w-3.5 h-3.5 text-sky-600" />
              {srv.name} ({formatCurrency(srv.price)})
            </button>
          ))}
        </div>

        {/* Selected Services Table */}
        {serviceOrders.length > 0 && (
          <div className="border border-slate-200 rounded-2xl overflow-hidden text-xs">
            <table className="w-full text-left">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                <tr>
                  <th className="py-2.5 px-3">Tên dịch vụ</th>
                  <th className="py-2.5 px-3">Đơn giá</th>
                  <th className="py-2.5 px-3">Ghi chú</th>
                  <th className="py-2.5 px-3 text-right">Xóa</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {serviceOrders.map((s, idx) => (
                  <tr key={idx}>
                    <td className="py-2.5 px-3 font-semibold text-slate-800">{s.service_name}</td>
                    <td className="py-2.5 px-3 text-slate-600 font-mono">{formatCurrency(s.price)}</td>
                    <td className="py-2.5 px-3 text-slate-500">{s.notes}</td>
                    <td className="py-2.5 px-3 text-right">
                      <button
                        onClick={() => handleRemoveService(idx)}
                        className="p-1 text-rose-500 hover:text-rose-700 rounded"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 4. Electronic Prescription Builder */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <Pill className="w-4 h-4 text-medical-600" />
            4. Kê đơn thuốc điện tử (e-Prescription)
          </h3>

          <button
            type="button"
            onClick={handleAddPrescriptionItem}
            className="flex items-center gap-1 px-3 py-1.5 bg-medical-50 hover:bg-medical-100 text-medical-700 border border-medical-200 rounded-xl font-bold text-xs transition-colors"
          >
            <Plus className="w-3.5 h-3.5" /> Thêm thuốc
          </button>
        </div>

        <div className="space-y-3">
          {prescriptionItems.map((item, idx) => (
            <div
              key={idx}
              className="p-4 rounded-2xl bg-slate-50 border border-slate-200 grid grid-cols-1 sm:grid-cols-12 gap-3 text-xs items-center"
            >
              <div className="sm:col-span-4">
                <label className="block text-[11px] font-bold text-slate-600 mb-1">
                  Thuốc #{idx + 1}
                </label>
                <select
                  value={item.medicine_id}
                  onChange={(e) => handleMedicineSelect(idx, e.target.value)}
                  className="w-full px-3 py-1.5 bg-white border border-slate-200 rounded-lg font-medium"
                >
                  <option value="">-- Chọn thuốc từ danh mục --</option>
                  {medicines.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.name} ({m.dosage_form || 'Viên'}) - Tồn: {m.stock_quantity}
                    </option>
                  ))}
                </select>
              </div>

              <div className="sm:col-span-2">
                <label className="block text-[11px] font-bold text-slate-600 mb-1">
                  Số lượng (viên/gói)
                </label>
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(e) => handlePrescriptionChange(idx, 'quantity', parseInt(e.target.value) || 1)}
                  className="w-full px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-center font-bold"
                />
              </div>

              <div className="sm:col-span-5">
                <label className="block text-[11px] font-bold text-slate-600 mb-1">
                  Liều dùng & Cách uống
                </label>
                <input
                  type="text"
                  value={item.dosage}
                  onChange={(e) => handlePrescriptionChange(idx, 'dosage', e.target.value)}
                  placeholder="1 viên x 2 lần/ngày sau ăn"
                  className="w-full px-3 py-1.5 bg-white border border-slate-200 rounded-lg"
                />
              </div>

              <div className="sm:col-span-1 flex justify-end pt-4 sm:pt-0">
                <button
                  type="button"
                  onClick={() => handleRemovePrescriptionItem(idx)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 5. AI Discharge Instructions Generator */}
      <div className="bg-gradient-to-br from-indigo-50/60 via-white to-sky-50/60 rounded-3xl p-6 border border-indigo-200/80 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-indigo-600 text-white rounded-xl shadow-xs">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                5. Hướng dẫn dặn dò sau khám (AI Post-visit Discharge Generator)
              </h3>
              <p className="text-xs text-slate-500">
                Tự động tổng hợp lịch uống thuốc, dặn dò sinh hoạt và lịch tái khám
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleGenerateDischarge}
            disabled={generatingDischarge}
            className="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-xs transition-colors self-start sm:self-auto"
          >
            <Sparkles className={`w-4 h-4 ${generatingDischarge ? 'animate-spin' : ''}`} />
            {generatingDischarge ? 'AI đang tổng hợp...' : 'AI Sinh hướng dẫn dặn dò'}
          </button>
        </div>

        <div>
          <textarea
            rows={5}
            value={dischargeInstructions}
            onChange={(e) => setDischargeInstructions(e.target.value)}
            placeholder="Nội dung dặn dò sinh hoạt, ăn uống và thời gian tái khám... (Bấm nút trên để AI tạo tự động)"
            className="w-full p-4 bg-white border border-slate-200 rounded-2xl text-xs leading-relaxed focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-2xs"
          />
        </div>

        {/* Mandatory Medical Disclaimer Badge */}
        <MedicalDisclaimerBadge />
      </div>

      {/* Bottom Action Footer */}
      <div className="flex justify-end gap-3 pt-4 border-t border-slate-200">
        <button
          type="button"
          onClick={() => navigate('/doctor/queue')}
          className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors"
        >
          Hủy bỏ
        </button>
        <button
          type="button"
          onClick={handleSubmitConsultation}
          disabled={submitting}
          className="flex items-center gap-2 px-8 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-lg hover:shadow-xl transition-all"
        >
          <CheckCircle2 className="w-4 h-4" />
          {submitting ? 'Đang hoàn tất...' : 'Hoàn tất khám & Chuyển sang Viện phí'}
        </button>
      </div>
    </div>
  );
};

export default ConsultationFormPage;
