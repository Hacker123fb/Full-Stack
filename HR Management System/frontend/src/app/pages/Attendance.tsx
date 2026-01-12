import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { CircleCheck, X, Clock } from 'lucide-react';
import {
  checkIn,
  checkOut,
  getTodayAttendance,
  getMyAttendanceHistory,
} from '../api';


/* ---------- TYPES ---------- */
type AttendanceRecord = {
  day: string;
  date: string;
  status: 'Present' | 'Leave' | 'Absent';
  checkIn: string;
  checkOut: string;
};

export function Attendance() {
  const navigate = useNavigate();
  const userRole = 'employee';

  const [isCheckedIn, setIsCheckedIn] = useState(false);
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const userName = 'Employee';

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  /* ---------- FETCH REAL ATTENDANCE ---------- */
  useEffect(() => {
  const fetchAttendance = async () => {
    try {
      console.log('Fetching today attendance...');
      const today = await getTodayAttendance();

      setIsCheckedIn(!!today.attendance?.check_in);

      console.log('Fetching attendance history...');
      const history = await getMyAttendanceHistory();

      const mapped = history.attendances.map((r: any) => ({
        day: new Date(r.date).toLocaleDateString('en-US', { weekday: 'long' }),
        date: r.date,
        status: r.status,
        checkIn: r.check_in ?? '-',
        checkOut: r.check_out ?? '-',
      }));

      setRecords(mapped);
    } catch (err) {
      console.error('Attendance fetch failed', err);
    } finally {
      setLoading(false);
    }
  };

  fetchAttendance();
}, []);


  /* ---------- CHECK-IN ---------- */
  const handleCheckIn = async () => {
    try {
      await checkIn();
      setIsCheckedIn(true);
    } catch (err) {
      console.error('Check-in failed', err);
    }
  };

  /* ---------- CHECK-OUT ---------- */
  const handleCheckOut = async () => {
    try {
      await checkOut();
      setIsCheckedIn(false);
    } catch (err) {
      console.error('Check-out failed', err);
    }
  };

  if (loading) {
    return <div className="p-8">Loading attendance...</div>;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole={userRole} onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName={userName} userRole="Employee" />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">
              Attendance
            </h1>

            {/* ---------- TODAY STATUS ---------- */}
            <Card className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Today's Attendance
              </h2>

              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 mb-2">Current Status</p>
                  <div className="flex items-center gap-2">
                    {isCheckedIn ? (
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

                <div className="flex gap-4">
                  {!isCheckedIn ? (
                    <Button onClick={handleCheckIn} variant="success">
                      Check In
                    </Button>
                  ) : (
                    <Button onClick={handleCheckOut} variant="danger">
                      Check Out
                    </Button>
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
                        Day
                      </th>
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
                    {records.map((record, index) => (
                      <tr key={index} className="border-b border-gray-100 last:border-0">
                        <td className="py-4 px-4 text-gray-800">{record.day}</td>
                        <td className="py-4 px-4 text-gray-600">{record.date}</td>
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
                              <X size={16} /> Absent
                            </span>
                          )}
                        </td>
                        <td className="py-4 px-4 text-gray-600">{record.checkIn}</td>
                        <td className="py-4 px-4 text-gray-600">{record.checkOut}</td>
                      </tr>
                    ))}
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
