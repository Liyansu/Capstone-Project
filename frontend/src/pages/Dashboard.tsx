import { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    api.get('/diet/summary').then((res) => setSummary(res.data));
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Welcome{user?.name ? `, ${user.name}` : ''}</h1>
        <button className="text-sm text-red-600" onClick={logout}>Logout</button>
      </div>
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
        <div className="p-4 rounded border">
          <div className="text-gray-500 text-sm">Calories Today</div>
          <div className="text-3xl font-bold">{summary?.calories_today ?? 0}</div>
        </div>
        <div className="p-4 rounded border">
          <div className="text-gray-500 text-sm">Compliance</div>
          <div className="text-3xl font-bold">{summary?.compliance ?? 0}%</div>
        </div>
      </div>
    </div>
  );
}
