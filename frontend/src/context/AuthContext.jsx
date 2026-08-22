import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const DEMO_ACCOUNTS = {
  admin: { username: 'admin', password: 'admin123', name: 'Quản trị viên Hệ thống', role: 'admin' },
  receptionist: { username: 'receptionist', password: 'rec123', name: 'Nguyễn Thị Thu Hà (Lễ tân)', role: 'receptionist' },
  doctor: { username: 'dr_nam', password: 'doc123', name: 'BS.CKII Nguyễn Văn Nam', role: 'doctor' },
  accountant: { username: 'accountant', password: 'acc123', name: 'Trần Bích Phương (Thu ngân)', role: 'accountant' },
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(true);

  // Initialize auth state
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      const data = response.data;
      
      const authToken = data.access_token;
      const userInfo = {
        id: data.user_id,
        username: data.username,
        full_name: data.full_name,
        role: data.role.toLowerCase(),
      };

      localStorage.setItem('token', authToken);
      localStorage.setItem('user', JSON.stringify(userInfo));

      setToken(authToken);
      setUser(userInfo);
      return { success: true, user: userInfo };
    } catch (error) {
      console.error('Login failed:', error);
      const detail = error.response?.data?.detail || 'Đăng nhập không thành công';
      return { success: false, error: detail };
    }
  };

  const quickLogin = async (roleKey) => {
    const acc = DEMO_ACCOUNTS[roleKey];
    if (!acc) return { success: false, error: 'Tài khoản không hợp lệ' };
    return await login(acc.username, acc.password);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  const role = user?.role || null;
  const isAuthenticated = !!token && !!user;

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        role,
        isAuthenticated,
        loading,
        login,
        quickLogin,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
