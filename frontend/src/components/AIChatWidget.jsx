import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, User, Sparkles, ChevronDown, HelpCircle, ShieldAlert } from 'lucide-react';
import { aiService } from '../services/aiService';
import MedicalDisclaimerBadge from './MedicalDisclaimerBadge';

const SAMPLE_QUESTIONS = [
  'Giờ làm việc của phòng khám như thế nào?',
  'Bệnh nhân có BHYT được giảm trừ bao nhiêu %?',
  'Quy trình khám bệnh và lấy số thứ tự ra sao?',
  'Bảng giá các dịch vụ xét nghiệm cơ bản?'
];

const AIChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Xin chào! Tôi là Trợ lý AI Hành chính của Phòng khám ICTU. Tôi có thể hỗ trợ bạn về lịch làm việc, quy trình tiếp đón, chính sách BHYT và bảng giá dịch vụ.',
      time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (textToSend = null) => {
    const query = (textToSend || inputText).trim();
    if (!query || loading) return;

    const userMsg = {
      sender: 'user',
      text: query,
      time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const response = await aiService.answerFAQ(query);
      const aiMsg = {
        sender: 'ai',
        text: response.answer || response.response || 'Tôi có thể hỗ trợ giải đáp quy trình hành chính và thủ tục của phòng khám.',
        disclaimer: response.disclaimer,
        isGuardrailTriggered: response.is_medical_diagnosis_refusal || false,
        time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error('FAQ AI Chat error:', err);
      // Resilient fallback rule answer
      let answerText = 'Phòng khám làm việc từ 07:30 - 17:00 (Thứ 2 đến Thứ 7). Quý khách có thể đặt hẹn trước qua hệ thống hoặc liên hệ quầy Lễ tân.';
      if (query.toLowerCase().includes('bảo hiểm') || query.toLowerCase().includes('bhyt')) {
        answerText = 'Phòng khám áp dụng BHYT đúng tuyến chi trả 80% - 100% danh mục theo quy định của Bộ Y Tế. Vui lòng xuất trình thẻ BHYT và CCCD gắn chip tại quầy lễ tân.';
      } else if (query.toLowerCase().includes('thuốc') || query.toLowerCase().includes('chẩn đoán') || query.toLowerCase().includes('bệnh gì')) {
        answerText = 'Trợ lý AI chỉ cung cấp thông tin hành chính và thủ tục quy trình. AI không có thẩm quyền chẩn đoán hoặc kê đơn thuốc. Vui lòng đăng ký khám với Bác sĩ chuyên khoa để được chẩn đoán chính xác.';
      }

      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: answerText,
          time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-40">
      {/* Floating Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="group relative flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-medical-600 to-sky-600 text-white rounded-full shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-200"
          title="Trợ lý AI Phòng khám"
        >
          <div className="relative">
            <Bot className="w-6 h-6" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 border-2 border-medical-700 rounded-full animate-ping"></span>
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 border-2 border-medical-700 rounded-full"></span>
          </div>
          <span className="font-semibold text-sm pr-1">Hỏi Trợ lý AI</span>
        </button>
      )}

      {/* Expanded Chat Dialog */}
      {isOpen && (
        <div className="bg-white rounded-2xl shadow-2xl border border-slate-200/90 w-[380px] sm:w-[420px] h-[580px] flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-300">
          {/* Header */}
          <div className="bg-gradient-to-r from-slate-900 via-medical-900 to-slate-800 text-white p-4 flex items-center justify-between shadow">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white/10 rounded-xl backdrop-blur-sm border border-white/20">
                <Bot className="w-6 h-6 text-sky-300" />
              </div>
              <div>
                <h3 className="font-bold text-sm flex items-center gap-1.5">
                  Trợ lý AI Hành chính
                  <span className="text-[10px] px-1.5 py-0.5 bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 rounded-full font-mono">
                    ONLINE
                  </span>
                </h3>
                <p className="text-[11px] text-slate-300">
                  Tư vấn quy trình, thủ tục BHYT & viện phí
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Quick Prompts Chips */}
          <div className="bg-sky-50/70 border-b border-sky-100 p-2.5 overflow-x-auto flex gap-1.5 no-scrollbar">
            {SAMPLE_QUESTIONS.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(q)}
                className="whitespace-nowrap text-[11px] font-medium bg-white hover:bg-sky-100 text-medical-800 border border-sky-200 px-2.5 py-1 rounded-full transition-colors shadow-2xs"
              >
                💬 {q}
              </button>
            ))}
          </div>

          {/* Messages Body */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-slate-50/60 text-xs">
            {messages.map((msg, index) => {
              const isAi = msg.sender === 'ai';
              return (
                <div
                  key={index}
                  className={`flex gap-2.5 ${isAi ? 'justify-start' : 'justify-end'}`}
                >
                  {isAi && (
                    <div className="w-7 h-7 rounded-full bg-medical-600 text-white flex items-center justify-center flex-shrink-0 shadow-xs mt-1">
                      <Bot className="w-4 h-4" />
                    </div>
                  )}

                  <div className={`max-w-[82%] space-y-1.5 ${isAi ? '' : 'text-right'}`}>
                    <div
                      className={`p-3 rounded-2xl text-xs leading-relaxed shadow-2xs ${
                        isAi
                          ? 'bg-white text-slate-800 border border-slate-200/80 rounded-tl-none'
                          : 'bg-medical-600 text-white rounded-tr-none'
                      }`}
                    >
                      <p className="whitespace-pre-line text-left">{msg.text}</p>
                    </div>

                    <div className="text-[10px] text-slate-400 px-1">
                      {msg.time}
                    </div>
                  </div>

                  {!isAi && (
                    <div className="w-7 h-7 rounded-full bg-slate-700 text-white flex items-center justify-center flex-shrink-0 shadow-xs mt-1">
                      <User className="w-4 h-4" />
                    </div>
                  )}
                </div>
              );
            })}

            {loading && (
              <div className="flex gap-2.5 items-center text-slate-400 italic text-xs">
                <Bot className="w-5 h-5 text-medical-500 animate-bounce" />
                <span>Trợ lý AI đang tra cứu quy trình...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Medical Disclaimer on Chat Footer */}
          <div className="px-3 py-1.5 bg-amber-50/90 border-t border-amber-200/80 text-[10px] text-amber-800 flex items-center gap-1.5">
            <ShieldAlert className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
            <span className="truncate">AI hỗ trợ hành chính, không chẩn đoán y khoa.</span>
          </div>

          {/* Input Footer */}
          <div className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Nhập câu hỏi về quy trình, BHYT, đặt lịch..."
              className="flex-1 text-xs border border-slate-200 rounded-xl px-3.5 py-2.5 focus:outline-none focus:ring-2 focus:ring-medical-500 focus:border-transparent bg-slate-50 focus:bg-white"
            />
            <button
              onClick={() => handleSend()}
              disabled={!inputText.trim() || loading}
              className="p-2.5 bg-medical-600 hover:bg-medical-700 disabled:opacity-50 text-white rounded-xl shadow-xs transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIChatWidget;
