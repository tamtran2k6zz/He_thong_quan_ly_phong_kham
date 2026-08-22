import React, { createContext, useContext, useState, useCallback } from 'react';
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from 'lucide-react';

const ToastContext = createContext(null);

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = Date.now() + Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toastSuccess = (msg, duration) => addToast(msg, 'success', duration);
  const toastError = (msg, duration) => addToast(msg, 'error', duration);
  const toastWarning = (msg, duration) => addToast(msg, 'warning', duration);
  const toastInfo = (msg, duration) => addToast(msg, 'info', duration);

  return (
    <ToastContext.Provider value={{ addToast, removeToast, toastSuccess, toastError, toastWarning, toastInfo }}>
      {children}
      {/* Toast Render Container */}
      <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-md w-full px-4 pointer-events-none">
        {toasts.map((toast) => {
          let bg = 'bg-slate-900 text-white';
          let icon = <Info className="w-5 h-5 text-sky-400 flex-shrink-0" />;

          if (toast.type === 'success') {
            bg = 'bg-emerald-800 text-emerald-50 border border-emerald-600';
            icon = <CheckCircle2 className="w-5 h-5 text-emerald-300 flex-shrink-0" />;
          } else if (toast.type === 'error') {
            bg = 'bg-rose-900 text-rose-50 border border-rose-700';
            icon = <AlertCircle className="w-5 h-5 text-rose-300 flex-shrink-0" />;
          } else if (toast.type === 'warning') {
            bg = 'bg-amber-900 text-amber-50 border border-amber-600';
            icon = <AlertTriangle className="w-5 h-5 text-amber-300 flex-shrink-0" />;
          }

          return (
            <div
              key={toast.id}
              className={`pointer-events-auto flex items-start gap-3 p-4 rounded-xl shadow-xl transition-all transform ease-out duration-300 ${bg}`}
            >
              {icon}
              <div className="flex-1 text-sm font-medium leading-relaxed">
                {toast.message}
              </div>
              <button
                onClick={() => removeToast(toast.id)}
                className="opacity-70 hover:opacity-100 transition-opacity p-0.5 rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};
