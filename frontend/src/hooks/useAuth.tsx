import { useEffect, useState } from 'react';
import api from '../services/api';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!localStorage.getItem('token'));
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    api.get('/users/me')
      .then((res) => setUser(res.data))
      .catch(() => {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
      });
  }, []);

  function login(token: string) {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  }

  function logout() {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
  }

  return { isAuthenticated, user, login, logout };
}
