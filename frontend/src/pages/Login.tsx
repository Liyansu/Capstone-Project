import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/auth/login', { email, password });
      login(res.data.token);
      navigate('/');
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-white p-6 rounded shadow">
        <h1 className="text-xl font-semibold mb-4">Login</h1>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <label className="block text-sm mb-1">Email</label>
        <input className="w-full border rounded px-3 py-2 mb-3" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label className="block text-sm mb-1">Password</label>
        <input className="w-full border rounded px-3 py-2 mb-4" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button disabled={loading} className="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50">
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <div className="text-sm mt-3">
          No account? <Link to="/register" className="text-blue-600">Register</Link>
        </div>
      </form>
    </div>
  );
}
