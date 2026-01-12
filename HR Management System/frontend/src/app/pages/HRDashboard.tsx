import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { Button } from '../components/Button';

import {
  getAllAttendance,
  approveLeave,
  rejectLeave,
} from '../api';


type Attendance = {
  id: number;
  employee_id: number;
  employee_name: string;
  status: string;
  date: string;
};

export function HRDashboard() {
  const navigate = useNavigate();
  const [records, setRecords] = useState<Attendance[]>([]);
  const [loading, setLoading] = useState(true);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getAllAttendance();
        setRecords(res.attendances || []);
      } catch (err) {
        console.error('Failed to load attendance', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="p-8">Loading HR Dashboard...</div>;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole="hr" onLogout={handleLogout} />

      <div className="flex-1 flex flex-col">
        <Header userName="HR Admin" userRole="HR" />

        <main className="p-8 overflow-y-auto">
          <h1 className="text-3xl font-bold mb-6">HR Attendance Control</h1>

          <Card>
            <table className="w-full">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Employee</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.id}>
                    <td>{r.date}</td>
                    <td>{r.employee_name}</td>
                    <td>{r.status}</td>
                    <td>
                      <Button
                        variant="success"
                        onClick={() => approveLeave(r.employee_id, r.date)}
                      >
                        Approve
                      </Button>
                      <Button
                        variant="danger"
                        onClick={() => rejectLeave(r.employee_id, r.date)}
                      >
                        Reject
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </main>
      </div>
    </div>
  );
}
