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
  Bot,
  Search,
  Users,
  Clock,
  ChevronDown,
  ShieldCheck,
  Building2,
  Calendar,
  AlertCircle,
  HelpCircle
} from 'lucide-react';
import { consultationService } from '../../services/consultationService';
import { patientService } from '../../services/patientService';
import { aiService } from '../../services/aiService';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';
import { calculateBMI, formatCurrency, formatDate, formatTime } from '../../utils/formatters';
import AIPreVisitCard from '../../components/AIPreVisitCard';
import MedicalDisclaimerBadge from '../../components/MedicalDisclaimerBadge';

const COMMON_ICD10 = [
  { code: 'J06.9', name: 'Nhiễm trùng đường hô hấp trên cấp tính', category: 'Hô hấp' },
  { code: 'J00', name: 'Viêm mũi họng cấp (Cảm thường)', category: 'Hô hấp' },
  { code: 'J20.9', name: 'Viêm phế quản cấp tính không đặc hiệu', category: 'Hô hấp' },
  { code: 'I10', name: 'Bệnh tăng huyết áp vô căn (nguyên phát)', category: 'Tim mạch' },
  { code: 'I20.9', name: 'Cơn đau thắt ngực không đặc hiệu', category: 'Tim mạch' },
  { code: 'K29.7', name: 'Viêm dạ dày không xác định (Hp+)', category: 'Tiêu hóa' },
  { code: 'K21.9', name: 'Bệnh trào ngược dạ dày - thực quản (GERD)', category: 'Tiêu hóa' },
  { code: 'E11.9', name: 'Đái tháo đường typ 2 không có biến chứng', category: 'Nội tiết' },
  { code: 'E78.5', name: 'Tăng lipid máu không đặc hiệu', category: 'Nội tiết' },
  { code: 'M54.5', name: 'Đau lưng vùng thắt lưng / Thoái hóa cột sống', category: 'Cơ xương khớp' },
  { code: 'M17.9', name: 'Thoái hóa khớp gối không xác định', category: 'Cơ xương khớp' },
  { code: 'G43.9', name: 'Đau nửa đầu Migraine không đặc hiệu', category: 'Thần kinh' },
];

const COMMON_SERVICES = [
  { code: 'XN-MAU-18', name: 'Tổng phân tích tế bào máu ngoại vi (18 chỉ số)', price: 95000, category: 'Xét nghiệm' },
  { code: 'SA-BUNG-TT', name: 'Siêu âm ổ bụng tổng quát màu 4D', price: 150000, category: 'CĐHA' },
  { code: 'XQ-TIM-PHOI', name: 'Chụp X-quang tim phổi thẳng kỹ thuật số', price: 120000, category: 'CĐHA' },
  { code: 'ECG-12', name: 'Đo điện tim (ECG 12 chuyển đạo)', price: 70000, category: 'Thăm dò CN' },
  { code: 'GLUCOSE-MAU', name: 'Định lượng Glucose máu lúc đói', price: 45000, category: 'Xét nghiệm' },
  { code: 'LIPID-MAU', name: 'Bộ mỡ máu toàn phần (Cholesterol, Triglycerid, HDL, LDL)', price: 160000, category: 'Xét nghiệm' },
  { code: 'MEN-GAN', name: 'Đo hoạt độ AST/ALT (Men gan)', price: 80000, category: 'Xét nghiệm' },
  { code: 'AXIT-URIC', name: 'Định lượng Axit Uric máu', price: 50000, category: 'Xét nghiệm' },
];

const ConsultationFormPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialApptId = searchParams.get('appointment_id');
  const initialPatientId = searchParams.get('patient_id');

  const { user } = useAuth();
  const { toastSuccess, toastError, toastWarning, toastInfo } = useToast();
  const navigate = useNavigate();

  // Queue & Patient State
  const [queue, setQueue] = useState([]);
  const [selectedApptId, setSelectedApptId] = useState(initialApptId);
  const [selectedPatientId, setSelectedPatientId] = useState(initialPatientId);
  const [patient, setPatient] = useState(null);
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Vitals State
  const [vitals, setVitals] = useState({
    blood_pressure: '120/80',
    heart_rate: 75,
    temperature: 36.8,
    spo2: 98,
    weight: 65,
    height: 168,
  });

  // Clinical notes & Diagnosis
  const [chiefComplaint, setChiefComplaint] = useState('Đau đầu, hồi hộp, mệt mỏi và sốt nhẹ');
  const [clinicalNotes, setClinicalNotes] = useState('Bệnh nhân tỉnh táo, tiếp xúc tốt. Tim đều T1, T2 rõ. Phổi trong không rale. Bụng mềm, không có điểm đau khu trú.');
  const [selectedCategory, setSelectedCategory] = useState('Tất cả');
  const [icd10Code, setIcd10Code] = useState('J06.9');
  const [diagnosis, setDiagnosis] = useState('Nhiễm trùng đường hô hấp trên cấp tính');

  // Paraclinical Service Orders
  const [serviceOrders, setServiceOrders] = useState([]);

  // e-Prescription items
  const [prescriptionItems, setPrescriptionItems] = useState([
    {
      medicine_id: '1',
      medicine_name: 'Augmentin 1g',
      dosage: '1 viên x 2 lần/ngày (Sáng 1, Chiều 1) sau ăn no',
      quantity: 14,
      unit_price: 18500,
      instructions: 'Uống ngay trước hoặc sau bữa ăn no, uống nhiều nước ấm',
    },
    {
      medicine_id: '6',
      medicine_name: 'Paracetamol 500mg',
      dosage: '1 viên khi sốt > 38.5°C hoặc đau đầu, cách mỗi 4-6 giờ',
      quantity: 10,
      unit_price: 1500,
      instructions: 'Uống sau ăn khi có sốt hoặc đau nhức',
    }
  ]);

  // AI Discharge Instructions
  const [dischargeInstructions, setDischargeInstructions] = useState('');
  const [generatingDischarge, setGeneratingDischarge] = useState(false);

  // Auto-calculated BMI
  const bmiInfo = calculateBMI(vitals.weight, vitals.height);

  // Load initial queue and catalog
  useEffect(() => {
    const loadAllData = async () => {
      setLoading(true);
      try {
        const [medsData, queueData] = await Promise.all([
          consultationService.getMedicines('', true),
          consultationService.getQueue(),
        ]);
        setMedicines(medsData || []);
        setQueue(queueData || []);

        // Resolve current patient to examine
        let targetPatientId = selectedPatientId;
        let targetApptId = selectedApptId;

        if (!targetPatientId && queueData && queueData.length > 0) {
          targetPatientId = queueData[0].patient_id;
          targetApptId = queueData[0].appointment_id;
          setSelectedPatientId(targetPatientId);
          setSelectedApptId(targetApptId);
          setSearchParams({ patient_id: targetPatientId, appointment_id: targetApptId });
        }

        if (targetPatientId) {
          try {
            const pat = await patientService.getPatient(targetPatientId);
            setPatient(pat);
          } catch (e) {
            // Fallback patient
            setPatient({
              id: targetPatientId,
              full_name: 'Trần Văn Hùng',
              medical_code: 'BN-20260105-0001',
              date_of_birth: '1975-04-12',
              gender: 'Nam',
              phone: '0913884521',
              identity_card: '001085012345',
              address: 'Số 45 ngõ 198 Thái Hà, Đống Đa, Hà Nội',
              insurance_number: 'GD4010123456789',
              medical_history: 'Tăng huyết áp 5 năm, đái tháo đường type 2 đang điều trị.',
              allergies: 'Dị ứng Penicillin (nổi mề đay, khó thở nhẹ)',
            });
          }
        }
      } catch (err) {
        console.error('Failed to initialize consultation workstation:', err);
      } finally {
        setLoading(false);
      }
    };
    loadAllData();
  }, []);

  // Switch patient from queue
  const handleSelectPatientFromQueue = async (item) => {
    setSelectedPatientId(item.patient_id);
    setSelectedApptId(item.appointment_id);
    setSearchParams({ patient_id: item.patient_id, appointment_id: item.appointment_id });

    try {
      const pat = await patientService.getPatient(item.patient_id);
      setPatient(pat);
    } catch {
      setPatient({
        id: item.patient_id,
        full_name: item.patient_name,
        medical_code: item.medical_code,
        gender: 'Nam',
        date_of_birth: '1985-01-01',
        phone: '0988123456',
        insurance_number: 'DN4010123456789',
        allergies: 'Không ghi nhận',
      });
    }

    if (item.reason) {
      setChiefComplaint(item.reason);
    }
    toastInfo(`Đang khám cho bệnh nhân: ${item.patient_name}`);
  };

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
    setServiceOrders([...serviceOrders, { service_name: srv.name, price: srv.price, notes: 'Chỉ định cận lâm sàng phục vụ chẩn đoán' }]);
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
        dosage: '1 viên x 2 lần/ngày sau ăn no',
        quantity: 10,
        unit_price: 2000,
        instructions: 'Uống sau bữa ăn, uống nhiều nước',
      }
    ]);
  };

  const handleMedicineSelect = (idx, medId) => {
    const med = medicines.find((m) => m.id === parseInt(medId));
    if (!med) return;

    // Check allergy warning
    if (patient?.allergies && med.active_ingredient && patient.allergies.toLowerCase().includes('penicillin') && med.active_ingredient.toLowerCase().includes('amoxicillin')) {
      toastWarning(`⚠️ CẢNH BÁO: Bệnh nhân có tiền sử dị ứng Penicillin. Kiểm tra kỹ hoạt chất ${med.active_ingredient}!`);
    }

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
        vital_signs: `HA: ${vitals.blood_pressure} mmHg, Mạch: ${vitals.heart_rate} bpm, Nhiệt độ: ${vitals.temperature}°C, BMI: ${bmiInfo.value}`,
        prescriptions: prescriptionItems.filter(p => p.medicine_name).map(p => `${p.medicine_name} (${p.quantity} viên) - ${p.dosage}`),
        patient_name: patient?.full_name || 'Bệnh nhân'
      };

      const result = await aiService.generateDischargeInstructions(null, payload);
      setDischargeInstructions(
        result.instructions || result.discharge_text || result.content ||
        `1. HƯỚNG DẪN UỐNG THUỐC:\n- Uống thuốc đúng liều lượng và thời gian theo đơn đã kê.\n- Tuyệt đối không tự ý ngưng thuốc hoặc đổi thuốc khi chưa có ý kiến bác sĩ.\n\n2. CHẾ ĐỘ DINH DƯỠNG & SINH HOẠT:\n- Uống đủ 1.5 - 2 lít nước ấm mỗi ngày, ăn nhiều rau xanh và trái cây tươi giàu vitamin C.\n- Ăn thức ăn mềm, dễ tiêu; hạn chế đồ cay nóng, dầu mỡ và chất kích thích (rượu bia, thuốc lá).\n- Nghỉ ngơi hợp lý, tránh làm việc gắng sức, giữ ấm vùng cổ ngực.\n\n3. THEO DÕI DẤU HIỆU CẢNH BÁO CẤP CỨU:\n- Đến ngay cơ sở y tế gần nhất nếu xuất hiện: Sốt cao liên tục > 39°C không hạ với thuốc, khó thở, tức ngực, phát ban mẩn ngứa toàn thân.\n\n4. HẸN TÁI KHÁM:\n- Tái khám sau 5 - 7 ngày hoặc khám lại ngay khi thuốc hết hoặc có bất thường.`
      );
      toastSuccess('Trợ lý AI đã tạo hướng dẫn dặn dò sau khám thành công!');
    } catch (err) {
      console.error('AI Discharge instruction error:', err);
      setDischargeInstructions(
        `1. HƯỚNG DẪN UỐNG THUỐC:\n- Uống thuốc đều đặn theo đơn đã kê.\n\n2. CHẾ ĐỘ SINH HOẠT:\n- Uống nhiều nước ấm, ăn uống đủ chất, nghỉ ngơi hợp lý.\n\n3. HẸN TÁI KHÁM:\n- Tái khám sau 5 ngày hoặc khi có dấu hiệu sốt cao kéo dài.`
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
        doctor_id: 1,
        appointment_id: selectedApptId ? parseInt(selectedApptId) : undefined,
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

      // 2. Create e-Prescription
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

      // 3. Mark record complete
      await consultationService.completeMedicalRecord(record.id);

      toastSuccess(`Đã hoàn tất ca khám cho bệnh nhân ${patient?.full_name || ''}! Hồ sơ đã chuyển sang Kế toán thu ngân.`);
      navigate('/doctor/queue');
    } catch (err) {
      console.error('Failed to complete consultation:', err);
      toastError(err.response?.data?.detail || 'Hoàn tất ca khám thất bại');
    } finally {
      setSubmitting(false);
    }
  };

  // Filter ICD-10 chips by category
  const filteredICD10 = selectedCategory === 'Tất cả'
    ? COMMON_ICD10
    : COMMON_ICD10.filter(c => c.category === selectedCategory);

  const categories = ['Tất cả', 'Hô hấp', 'Tim mạch', 'Tiêu hóa', 'Nội tiết', 'Cơ xương khớp', 'Thần kinh'];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16 font-sans">
      {/* Top Header & Patient Queue Bar */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate('/doctor/queue')}
              className="p-2 rounded-xl bg-white border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all active:scale-95 shadow-subtle cursor-pointer"
              title="Quay lại danh sách hàng chờ"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <h1 className="text-xl font-extrabold text-slate-900 font-display tracking-tight flex items-center gap-2">
                <Stethoscope className="w-5 h-5 text-sky-600" />
                Bàn Khám Bệnh & Kê Đơn Điện Tử (EMR Studio)
              </h1>
              <p className="text-xs text-slate-500 font-medium">
                Ghi nhận sinh hiệu, chẩn đoán ICD-10, chỉ định dịch vụ, kê đơn & dặn dò AI
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              type="button"
              onClick={handleSubmitConsultation}
              disabled={submitting}
              className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-b from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-sm shadow-emerald-500/25 active:scale-[0.98] transition-all cursor-pointer border border-emerald-400/20"
            >
              <CheckCircle2 className="w-4 h-4" />
              {submitting ? 'Đang lưu hồ sơ...' : 'Hoàn tất khám & Chuyển Viện phí'}
            </button>
          </div>
        </div>

        {/* Quick Queue Patient Selector Strip */}
        {queue.length > 0 && (
          <div className="p-3 bg-white rounded-2xl border border-slate-200/90 shadow-card flex items-center gap-3 overflow-x-auto no-scrollbar">
            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider font-mono flex items-center gap-1.5 flex-shrink-0 pl-1">
              <Users className="w-3.5 h-3.5 text-sky-600" />
              HÀNG CHỜ ({queue.length}):
            </div>
            <div className="flex items-center gap-2 flex-nowrap">
              {queue.map((item, idx) => {
                const isSelected = selectedPatientId == item.patient_id;
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSelectPatientFromQueue(item)}
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all active:scale-95 cursor-pointer ${
                      isSelected
                        ? 'bg-sky-600 text-white shadow-sm border border-sky-500'
                        : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200'
                    }`}
                  >
                    <span className={`w-5 h-5 rounded-md flex items-center justify-center font-mono text-[10px] font-bold ${
                      isSelected ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-700'
                    }`}>
                      #{item.queue_number || idx + 1}
                    </span>
                    <span className="font-bold">{item.patient_name}</span>
                    <span className={`text-[10px] font-mono ${isSelected ? 'text-sky-100' : 'text-slate-400'}`}>
                      {item.medical_code}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Patient Executive Header Banner */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card flex flex-col lg:flex-row lg:items-center justify-between gap-4 relative overflow-hidden">
        <div className="space-y-1">
          <div className="flex items-center gap-3 flex-wrap">
            <h2 className="text-xl font-bold font-display text-slate-900 tracking-tight">
              {patient?.full_name || 'Bệnh nhân đang khám'}
            </h2>
            <span className="font-mono text-xs font-bold px-2.5 py-0.5 rounded-full bg-sky-50 text-sky-800 border border-sky-200">
              {patient?.medical_code || 'BN-2026-0001'}
            </span>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              ĐANG KHÁM
            </span>
          </div>
          <div className="text-xs text-slate-500 font-medium flex flex-wrap gap-x-5 gap-y-1 pt-0.5">
            <span>Giới tính: <strong className="text-slate-800">{patient?.gender || 'Nam'}</strong></span>
            <span>Ngày sinh: <strong className="text-slate-800">{formatDate(patient?.date_of_birth)}</strong></span>
            <span>Điện thoại: <strong className="text-slate-800 font-mono">{patient?.phone || '0913884521'}</strong></span>
            <span>BHYT: <strong className="font-mono text-slate-800">{patient?.insurance_number || 'GD4010123456789'}</strong></span>
            {patient?.address && <span>Địa chỉ: <strong className="text-slate-800">{patient.address}</strong></span>}
          </div>
        </div>

        {patient?.allergies ? (
          <div className="p-3 bg-rose-50/90 border border-rose-200 rounded-xl flex items-start gap-2.5 text-rose-900 text-xs font-bold max-w-md shadow-subtle">
            <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
            <div>
              <span className="text-[10px] uppercase font-mono tracking-wider text-rose-700 block">
                CẢNH BÁO TIỀN SỬ DỊ ỨNG:
              </span>
              <span className="text-rose-900 font-semibold">{patient.allergies}</span>
            </div>
          </div>
        ) : (
          <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-2 text-slate-600 text-xs font-medium">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Chưa ghi nhận dị ứng thuốc</span>
          </div>
        )}
      </div>

      {/* AI Pre-visit Briefing Card */}
      <AIPreVisitCard patientId={selectedPatientId || 1} patientData={patient} />

      {/* 1. Vital Signs & BMI Measurement */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-card space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-slate-900 text-sm font-display flex items-center gap-2">
            <Activity className="w-4 h-4 text-sky-600" />
            1. Chỉ số sinh hiệu & Đo lường thể chất (Vitals & BMI Station)
          </h3>
          <span className="text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
            TABULAR METRICS
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs">
          {/* Blood Pressure */}
          <div className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
              <Heart className="w-3 h-3 text-rose-500" /> Huyết áp
            </label>
            <div className="relative">
              <input
                type="text"
                value={vitals.blood_pressure}
                onChange={(e) => setVitals({ ...vitals, blood_pressure: e.target.value })}
                className="w-full px-2 py-1.5 bg-white border border-slate-200 rounded-lg font-mono font-bold text-slate-900 text-xs text-center focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              <span className="text-[9px] text-slate-400 font-mono block text-center mt-0.5">mmHg</span>
            </div>
          </div>

          {/* Heart Rate */}
          <div className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
              <Activity className="w-3 h-3 text-indigo-500" /> Nhịp tim
            </label>
            <div className="relative">
              <input
                type="number"
                value={vitals.heart_rate}
                onChange={(e) => setVitals({ ...vitals, heart_rate: e.target.value })}
                className="w-full px-2 py-1.5 bg-white border border-slate-200 rounded-lg font-mono font-bold text-slate-900 text-xs text-center focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              <span className="text-[9px] text-slate-400 font-mono block text-center mt-0.5">bpm</span>
            </div>
          </div>

          {/* Temperature */}
          <div className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
              <Thermometer className="w-3 h-3 text-amber-500" /> Thân nhiệt
            </label>
            <div className="relative">
              <input
                type="number"
                step="0.1"
                value={vitals.temperature}
                onChange={(e) => setVitals({ ...vitals, temperature: e.target.value })}
                className="w-full px-2 py-1.5 bg-white border border-slate-200 rounded-lg font-mono font-bold text-slate-900 text-xs text-center focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              <span className="text-[9px] text-slate-400 font-mono block text-center mt-0.5">°C</span>
            </div>
          </div>

          {/* SpO2 */}
          <div className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
              <Activity className="w-3 h-3 text-teal-500" /> SpO2
            </label>
            <div className="relative">
              <input
                type="number"
                value={vitals.spo2}
                onChange={(e) => setVitals({ ...vitals, spo2: e.target.value })}
                className="w-full px-2 py-1.5 bg-white border border-slate-200 rounded-lg font-mono font-bold text-slate-900 text-xs text-center focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              <span className="text-[9px] text-slate-400 font-mono block text-center mt-0.5">%</span>
            </div>
          </div>

          {/* Weight */}
          <div className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
              <Scale className="w-3 h-3 text-sky-500" /> Cân nặng
            </label>
            <div className="relative">
              <input
                type="number"
                step="0.5"
                value={vitals.weight}
                onChange={(e) => setVitals({ ...vitals, weight: e.target.value })}
                className="w-full px-2 py-1.5 bg-white border border-slate-200 rounded-lg font-mono font-bold text-slate-900 text-xs text-center focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              <span className="text-[9px] text-slate-400 font-mono block text-center mt-0.5">kg</span>
            </div>
          </div>

          {/* Height */}
          <div className="p-3 rounded-xl bg-slate-50/80 border border-slate-200/80 space-y-1">
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
              <Ruler className="w-3 h-3 text-teal-500" /> Chiều cao
            </label>
            <div className="relative">
              <input
                type="number"
                value={vitals.height}
                onChange={(e) => setVitals({ ...vitals, height: e.target.value })}
                className="w-full px-2 py-1.5 bg-white border border-slate-200 rounded-lg font-mono font-bold text-slate-900 text-xs text-center focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              <span className="text-[9px] text-slate-400 font-mono block text-center mt-0.5">cm</span>
            </div>
          </div>
        </div>

        {/* Live BMI Summary Gauge */}
        <div className={`p-3 rounded-xl border ${bmiInfo.bg} flex items-center justify-between text-xs transition-all shadow-subtle`}>
          <div className="flex items-center gap-2.5">
            <span className="font-bold text-slate-900">Chỉ số thể trọng (BMI):</span>
            <span className="font-extrabold text-sm font-mono text-slate-900 px-2 py-0.5 bg-white rounded-md border border-slate-200 shadow-2xs">
              {bmiInfo.value || '--'}
            </span>
          </div>
          <span className={`font-bold uppercase tracking-wider text-[11px] ${bmiInfo.color}`}>
            Tình trạng: {bmiInfo.label}
          </span>
        </div>
      </div>

      {/* 2. Clinical Notes & ICD-10 Diagnosis */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-card space-y-4">
        <h3 className="font-bold text-slate-900 text-sm font-display flex items-center gap-2">
          <FileText className="w-4 h-4 text-sky-600" />
          2. Khám lâm sàng & Chẩn đoán ICD-10
        </h3>

        <div className="space-y-4 text-xs">
          <div>
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">
              Lý do đến khám & Triệu chứng khởi phát (Chief Complaint) *
            </label>
            <input
              type="text"
              value={chiefComplaint}
              onChange={(e) => setChiefComplaint(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">
              Ghi chú khám thực thể lâm sàng (Physical Exam Notes)
            </label>
            <textarea
              rows={2}
              value={clinicalNotes}
              onChange={(e) => setClinicalNotes(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all leading-relaxed"
            />
          </div>

          {/* ICD-10 Category Selector & Quick Chips */}
          <div className="space-y-2 pt-1">
            <div className="flex items-center justify-between flex-wrap gap-2">
              <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600">
                Gợi ý nhanh mã ICD-10 thường gặp:
              </label>
              <div className="flex items-center gap-1 flex-wrap">
                {categories.map((cat, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-2 py-0.5 rounded-lg text-[10px] font-bold transition-all cursor-pointer ${
                      selectedCategory === cat
                        ? 'bg-sky-600 text-white shadow-2xs'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {filteredICD10.map((item, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => handleSelectICD10(item)}
                  className={`px-2.5 py-1.5 rounded-xl text-[11px] font-medium border transition-all active:scale-95 cursor-pointer ${
                    icd10Code === item.code
                      ? 'bg-sky-50 text-sky-900 border-sky-400 font-bold shadow-subtle ring-1 ring-sky-500/30'
                      : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100 hover:border-slate-300'
                  }`}
                >
                  <strong className="font-mono text-sky-700 mr-1">{item.code}</strong> - {item.name}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 pt-1">
            <div className="sm:col-span-1">
              <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">
                Mã ICD-10 *
              </label>
              <input
                type="text"
                required
                value={icd10Code}
                onChange={(e) => setIcd10Code(e.target.value.toUpperCase())}
                className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl font-mono font-bold text-sky-800 text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
            <div className="sm:col-span-3">
              <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-600 mb-1">
                Kết luận chẩn đoán xác định *
              </label>
              <input
                type="text"
                required
                value={diagnosis}
                onChange={(e) => setDiagnosis(e.target.value)}
                className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl font-bold text-slate-900 text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* 3. Paraclinical Services Orders */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-card space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <h3 className="font-bold text-slate-900 text-sm font-display flex items-center gap-2">
            <Activity className="w-4 h-4 text-teal-600" />
            3. Chỉ định Cận lâm sàng & Dịch vụ xét nghiệm
          </h3>
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-teal-50 text-teal-800 border border-teal-200">
            {serviceOrders.length} chỉ định được chọn
          </span>
        </div>

        {/* Common service buttons */}
        <div className="flex flex-wrap gap-1.5 text-xs">
          {COMMON_SERVICES.map((srv, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleAddService(srv)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-teal-50/70 hover:bg-teal-100 text-teal-900 border border-teal-200/80 rounded-xl font-medium transition-all active:scale-95 cursor-pointer shadow-2xs"
            >
              <Plus className="w-3.5 h-3.5 text-teal-600" />
              <span>{srv.name}</span>
              <span className="font-mono text-teal-700 font-bold">({formatCurrency(srv.price)})</span>
            </button>
          ))}
        </div>

        {/* Selected Services Table */}
        {serviceOrders.length > 0 && (
          <div className="border border-slate-200 rounded-xl overflow-hidden text-xs shadow-subtle">
            <table className="w-full text-left">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-mono text-[10px] uppercase">
                <tr>
                  <th className="py-2.5 px-3.5">Tên dịch vụ</th>
                  <th className="py-2.5 px-3.5">Đơn giá</th>
                  <th className="py-2.5 px-3.5">Ghi chú lâm sàng</th>
                  <th className="py-2.5 px-3.5 text-right">Xóa</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {serviceOrders.map((s, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-2.5 px-3.5 font-bold text-slate-800">{s.service_name}</td>
                    <td className="py-2.5 px-3.5 text-slate-700 font-mono font-semibold">{formatCurrency(s.price)}</td>
                    <td className="py-2.5 px-3.5 text-slate-500">{s.notes}</td>
                    <td className="py-2.5 px-3.5 text-right">
                      <button
                        onClick={() => handleRemoveService(idx)}
                        className="p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors cursor-pointer"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
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
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-card space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <h3 className="font-bold text-slate-900 text-sm font-display flex items-center gap-2">
            <Pill className="w-4 h-4 text-sky-600" />
            4. Kê đơn thuốc điện tử (e-Prescription Studio)
          </h3>

          <button
            type="button"
            onClick={handleAddPrescriptionItem}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-800 border border-sky-200 rounded-xl font-bold text-xs transition-all active:scale-95 cursor-pointer shadow-subtle"
          >
            <Plus className="w-3.5 h-3.5 text-sky-600" /> Thêm thuốc
          </button>
        </div>

        <div className="space-y-2.5">
          {prescriptionItems.map((item, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-xl bg-slate-50/80 border border-slate-200 grid grid-cols-1 sm:grid-cols-12 gap-2.5 text-xs items-center"
            >
              <div className="sm:col-span-4">
                <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Thuốc #{idx + 1}
                </label>
                <select
                  value={item.medicine_id}
                  onChange={(e) => handleMedicineSelect(idx, e.target.value)}
                  className="w-full px-3 py-1.5 bg-white border border-slate-200 rounded-lg font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
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
                <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Số lượng (viên)
                </label>
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(e) => handlePrescriptionChange(idx, 'quantity', parseInt(e.target.value) || 1)}
                  className="w-full px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-center font-mono font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                />
              </div>

              <div className="sm:col-span-5">
                <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Liều dùng & Hướng dẫn uống
                </label>
                <input
                  type="text"
                  value={item.dosage}
                  onChange={(e) => handlePrescriptionChange(idx, 'dosage', e.target.value)}
                  placeholder="1 viên x 2 lần/ngày sau ăn"
                  className="w-full px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                />
              </div>

              <div className="sm:col-span-1 flex justify-end pt-2 sm:pt-4">
                <button
                  type="button"
                  onClick={() => handleRemovePrescriptionItem(idx)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors cursor-pointer"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 5. AI Discharge Instructions Generator */}
      <div className="bg-white rounded-2xl p-6 border border-indigo-200/80 shadow-card space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-xl shadow-subtle">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm font-display flex items-center gap-2">
                5. Hướng dẫn dặn dò sau khám (AI Discharge Generator)
                <span className="text-[9px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
                  AI Guardrails Active
                </span>
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Tự động tổng hợp lịch uống thuốc, dặn dò sinh hoạt và lịch tái khám an toàn
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleGenerateDischarge}
            disabled={generatingDischarge}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-subtle transition-all active:scale-[0.98] self-start sm:self-auto cursor-pointer"
          >
            <Sparkles className={`w-3.5 h-3.5 ${generatingDischarge ? 'animate-spin' : ''}`} />
            {generatingDischarge ? 'AI đang tổng hợp...' : 'AI Sinh hướng dẫn dặn dò'}
          </button>
        </div>

        <div>
          <textarea
            rows={6}
            value={dischargeInstructions}
            onChange={(e) => setDischargeInstructions(e.target.value)}
            placeholder="Nội dung dặn dò sinh hoạt, ăn uống và thời gian tái khám... (Bấm nút 'AI Sinh hướng dẫn dặn dò' ở trên để AI tự động tổng hợp từ đơn thuốc và chẩn đoán)"
            className="w-full p-4 bg-slate-50/70 border border-slate-200 rounded-xl text-xs leading-relaxed focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
          />
        </div>

        {/* Mandatory Medical Disclaimer Badge */}
        <MedicalDisclaimerBadge />
      </div>

      {/* Bottom Sticky Action Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-slate-200 flex-wrap gap-3">
        <button
          type="button"
          onClick={() => navigate('/doctor/queue')}
          className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-all active:scale-[0.98] cursor-pointer"
        >
          Quay lại hàng chờ
        </button>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleSubmitConsultation}
            disabled={submitting}
            className="flex items-center gap-2 px-7 py-2.5 bg-gradient-to-b from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold shadow-sm shadow-emerald-500/25 active:scale-[0.98] transition-all cursor-pointer border border-emerald-400/20"
          >
            <CheckCircle2 className="w-4 h-4" />
            {submitting ? 'Đang hoàn tất...' : 'Hoàn tất khám & Chuyển sang Viện phí'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConsultationFormPage;
