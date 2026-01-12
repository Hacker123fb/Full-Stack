import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { CircleCheck, X, Clock } from 'lucide-react';
import {
  employeeCheckIn,
  employeeCheckOut,
  getTodayAttendance,
  getMyAttendanceHistory,
} from '../api';

/* ---------- TYPES ---------- */
type AttendanceRecord = {
  date: string;
  status: 'Present' | 'Absent' | 'Leave' | 'Half-day';
  checkIn: string;
  checkOut: string;
};
const formatTime = (time: string | null) => {
  if (!time || time === '-') return '-';

  const [hours, minutes, seconds] = time.split(':').map(Number);
  const date = new Date();
  date.setHours(hours, minutes, seconds || 0);

  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
};

export function EmployeeAttendance() {
  const navigate = useNavigate();
  const userRole = 'employee';

  const [today, setToday] = useState<any>(null);
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  /* ---------- FETCH ATTENDANCE ---------- */
  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        // ✅ Today
        const todayRes = await getTodayAttendance();
        setToday(todayRes.attendance);

        // ✅ History
        const historyRes = await getMyAttendanceHistory();
        const mapped: AttendanceRecord[] = (historyRes.attendances || []).map(
          (r: any) => ({
            date: r.date,
            status: r.status,
            checkIn: r.check_in ?? '-',
            checkOut: r.check_out ?? '-',
          })
        );

        setRecords(mapped);
      } catch (err) {
        console.error('Attendance fetch failed', err);
        setRecords([]);
      } finally {
        setLoading(false);
      }
    };

    fetchAttendance();
  }, []);

  /* ---------- CHECK-IN ---------- */
  const handleCheckIn = async () => {
    try {
      setActionLoading(true);
      const res = await employeeCheckIn();
      setToday(res.attendance);
    } catch (err) {
      console.error('Check-in failed', err);
    } finally {
      setActionLoading(false);
    }
  };

  /* ---------- CHECK-OUT ---------- */
  const handleCheckOut = async () => {
    try {
      setActionLoading(true);
      const res = await employeeCheckOut();
      setToday(res.attendance);
    } catch (err) {
      console.error('Check-out failed', err);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8">Loading attendance...</div>;
  }

  const isCheckedIn = !!today?.check_in && !today?.check_out;
  const isCheckedOut = !!today?.check_out;
{today?.check_in && !today?.check_out && (
  <p className="text-sm text-gray-500 mt-2">
    Checked in at {formatTime(today.check_in)}
  </p>
)}
{today?.check_out && (
  <p className="text-sm text-gray-500 mt-2">
    Checked out at {formatTime(today.check_out)}
  </p>
)}

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole={userRole} onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName="Employee" userRole="Employee" />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">
              My Attendance
            </h1>

            {/* ---------- TODAY STATUS ---------- */}
            <Card className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Today’s Attendance
              </h2>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 mb-2">Current Status</p>
                  <div className="flex items-center gap-2">
                    {isCheckedOut ? (
                      <>
                        <CircleCheck className="text-green-600" size={24} />
                        <span className="text-lg font-semibold text-green-600">
                          Checked Out
                        </span>
                      </>
                    ) : isCheckedIn ? (
                      <>
                        <CircleCheck className="text-green-600" size={24} />
                        <span className="text-lg font-semibold text-green-600">
                          Checked In
                        </span>
                      </>
                    ) : (
                      <>
                        <Clock className="text-gray-600" size={24} />
                        <span className="text-lg font-semibold text-gray-600">
                          Not Checked In
                        </span>
                      </>
                    )}
                  </div>
                </div>

                <div>
                  {!today && (
                    <Button
                      onClick={handleCheckIn}
                      variant="success"
                      disabled={actionLoading}
                    >
                      Check In
                    </Button>
                  )}

                  {isCheckedIn && (
                    <Button
                      onClick={handleCheckOut}
                      variant="danger"
                      disabled={actionLoading}
                    >
                      Check Out
                    </Button>
                  )}

                  {isCheckedOut && (
                    <span className="text-gray-500 font-medium">
                      Attendance completed for today
                    </span>
                  )}
                </div>
              </div>
            </Card>

            {/* ---------- ATTENDANCE HISTORY ---------- */}
            <Card>
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Attendance History
              </h2>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b border-gray-200">
                    <tr>
                      <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">
                        Date
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">
                        Status
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">
                        Check In
                      </th>
                      <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">
                        Check Out
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {records.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="text-center py-6 text-gray-500">
                          No attendance records found
                        </td>
                      </tr>
                    ) : (
                      records.map((record, index) => (
                        <tr
                          key={index}
                          className="border-b border-gray-100 last:border-0"
                        >
                          <td className="py-4 px-4 text-gray-800">
                            {record.date}
                          </td>

                          <td className="py-4 px-4">
                            {record.status === 'Present' ? (
                              <span className="flex items-center gap-2 text-green-600">
                                <CircleCheck size={16} /> Present
                              </span>
                            ) : record.status === 'Leave' ? (
                              <span className="flex items-center gap-2 text-orange-600">
                                <Clock size={16} /> Leave
                              </span>
                            ) : (
                              <span className="flex items-center gap-2 text-red-600">
                                <X size={16} /> {record.status}
                              </span>
                            )}
                          </td>

                          <td className="py-4 px-4 text-gray-600">
                          {formatTime(record.checkIn)}
                         </td>
                         <td className="py-4 px-4 text-gray-600">
                         {formatTime(record.checkOut)}
                         </td>
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
