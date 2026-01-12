import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';

import {
  getAdminStats,
  getAllUsers,
} from '../api';

/* ---------- TYPES ---------- */
type AdminStats = {
  total_users: number;
  total_employees: number;
  total_attendance_records: number;
};

type User = {
  id: number;
  email: string;
  role: string;
};

/* ---------- COMPONENT ---------- */
export function AdminDashboard() {
  const navigate = useNavigate();

  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  /* ---------- FETCH ADMIN DATA ---------- */
  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const statsRes = await getAdminStats();
        const usersRes = await getAllUsers();

        setStats(statsRes);
        setUsers(usersRes.users || []);
      } catch (err: any) {
        console.error('Admin data load failed', err);
        setError('Failed to load admin data. Check backend & CORS.');
      } finally {
        setLoading(false);
      }
    };

    fetchAdminData();
  }, []);

  /* ---------- RENDER GUARDS ---------- */
  if (loading) {
    return <div className="p-8 text-lg">Loading Admin Dashboard…</div>;
  }

  if (error) {
    return (
      <div className="p-8 text-red-600">
        <p className="font-bold">Admin Dashboard Error</p>
        <p>{error}</p>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-8 text-red-600">
        Failed to load admin statistics.
      </div>
    );
  }

  /* ---------- UI ---------- */
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole="admin" onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName="Admin" userRole="Administrator" />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">

            <h1 className="text-3xl font-bold text-gray-800 mb-8">
              Admin Dashboard
            </h1>

            {/* ---------- STATS ---------- */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <Card>
                <p className="text-sm text-gray-500">Total Users</p>
                <p className="text-2xl font-bold">{stats.total_users}</p>
              </Card>

              <Card>
                <p className="text-sm text-gray-500">Employees</p>
                <p className="text-2xl font-bold">{stats.total_employees}</p>
              </Card>

              <Card>
                <p className="text-sm text-gray-500">Attendance Records</p>
                <p className="text-2xl font-bold">
                  {stats.total_attendance_records}
                </p>
              </Card>
            </div>

            {/* ---------- USER LIST ---------- */}
            <Card>
              <h2 className="text-xl font-semibold mb-4">All Users</h2>

              <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-3">ID</th>
                      <th className="text-left p-3">Email</th>
                      <th className="text-left p-3">Role</th>
                    </tr>
                  </thead>

                  <tbody>
                    {users.length === 0 ? (
                      <tr>
                        <td colSpan={3} className="p-4 text-center text-gray-500">
                          No users found
                        </td>
                      </tr>
                    ) : (
                      users.map((u) => (
                        <tr key={u.id} className="border-b">
                          <td className="p-3">{u.id}</td>
                          <td className="p-3">{u.email}</td>
                          <td className="p-3">{u.role}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </Card>

          </div>
        </main>
      </div>
    </div>
  );
}
