import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { CircleCheck, X, Clock } from 'lucide-react';
import { getAllAttendance, approveLeave, rejectLeave } from '../api';

type AttendanceRow = {
  id: number;
  employee_id: number;
  employee_name: string;
  department: string;
  date: string;
  status: string;
  check_in: string | null;
  check_out: string | null;
};

export function HRAttendance() {
  const navigate = useNavigate();
  const userRole = 'admin';

  const [data, setData] = useState<AttendanceRow[]>([]);
  const [loading, setLoading] = useState(true);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const fetchAttendance = async () => {
    try {
      setLoading(true);
      const res = await getAllAttendance();
      setData(res.attendances || []);
    } catch (err) {
      console.error('Failed to load attendance', err);
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttendance();
  }, []);

  const handleApprove = async (empId: number, date: string) => {
    await approveLeave(empId, date);
    fetchAttendance();
  };

  const handleReject = async (empId: number, date: string) => {
    await rejectLeave(empId, date);
    fetchAttendance();
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole={userRole} onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName="HR Admin" userRole="Administrator" />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">
              Attendance Management
            </h1>

            <Card>
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Employee Attendance
              </h2>

              {loading ? (
                <p>Loading attendance...</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="border-b border-gray-200">
                      <tr>
                        <th className="px-4 py-3 text-left">Employee</th>
                        <th className="px-4 py-3 text-left">Department</th>
                        <th className="px-4 py-3 text-left">Date</th>
                        <th className="px-4 py-3 text-left">Status</th>
                        <th className="px-4 py-3 text-left">Action</th>
                      </tr>
                    </thead>

                    <tbody>
                      {data.length === 0 ? (
                        <tr>
                          <td colSpan={5} className="text-center py-6">
                            No records found
                          </td>
                        </tr>
                      ) : (
                        data.map((row) => (
                          <tr key={row.id} className="border-b">
                            <td className="px-4 py-3">
                              {row.employee_name}
                            </td>
                            <td className="px-4 py-3">
                              {row.department}
                            </td>
                            <td className="px-4 py-3">
                              {row.date}
                            </td>
                            <td className="px-4 py-3">
                              {row.status === 'Present' ? (
                                <span className="text-green-600 flex items-center gap-2">
                                  <CircleCheck size={16} /> Present
                                </span>
                              ) : row.status === 'Leave' ? (
                                <span className="text-orange-600 flex items-center gap-2">
                                  <Clock size={16} /> Leave
                                </span>
                              ) : (
                                <span className="text-red-600 flex items-center gap-2">
                                  <X size={16} /> Absent
                                </span>
                              )}
                            </td>
                            <td className="px-4 py-3">
                              {row.status === 'Leave' ? (
                                <div className="flex gap-2">
                                  <Button
                                    variant="success"
                                    onClick={() =>
                                      handleApprove(
                                        row.employee_id,
                                        row.date
                                      )
                                    }
                                  >
                                    Approve
                                  </Button>
                                  <Button
                                    variant="danger"
                                    onClick={() =>
                                      handleReject(
                                        row.employee_id,
                                        row.date
                                      )
                                    }
                                  >
                                    Reject
                                  </Button>
                                </div>
                              ) : (
                                <span className="text-gray-500">
                                  —
                                </span>
                              )}
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}
