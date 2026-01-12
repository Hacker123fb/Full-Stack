import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Select } from '../components/Select';
import { apiRequest } from '../api';

export function LeaveManagement() {
  const navigate = useNavigate();
  const userName = localStorage.getItem('userName') || 'User';
  const userRole = (localStorage.getItem('userRole') as 'employee' | 'admin') || 'employee';

  const [formData, setFormData] = useState({
    leaveType: 'sick',
    startDate: '',
    endDate: '',
    remarks: '',
  });

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Leave request submitted successfully!');
    setFormData({
      leaveType: 'sick',
      startDate: '',
      endDate: '',
      remarks: '',
    });
  };

  const leaveHistory = [
    { id: 1, type: 'Sick Leave', dates: 'Dec 15 - Dec 17, 2024', status: 'Approved', color: 'bg-green-100 text-green-700' },
    { id: 2, type: 'Vacation', dates: 'Jan 5 - Jan 10, 2025', status: 'Pending', color: 'bg-yellow-100 text-yellow-700' },
    { id: 3, type: 'Personal', dates: 'Nov 22, 2024', status: 'Rejected', color: 'bg-red-100 text-red-700' },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole={userRole} onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName={userName} userRole={userRole === 'admin' ? 'Administrator' : 'Employee'} />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">Leave Management</h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Apply Leave Form */}
              <Card>
                <h2 className="text-xl font-semibold text-gray-800 mb-6">Apply for Leave</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <Select
                    label="Leave Type"
                    value={formData.leaveType}
                    onChange={(e) => setFormData({ ...formData, leaveType: e.target.value })}
                    options={[
                      { value: 'sick', label: 'Sick Leave' },
                      { value: 'vacation', label: 'Vacation' },
                      { value: 'personal', label: 'Personal Leave' },
                      { value: 'emergency', label: 'Emergency Leave' },
                    ]}
                  />

                  <Input
                    label="Start Date"
                    type="date"
                    value={formData.startDate}
                    onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                    required
                  />

                  <Input
                    label="End Date"
                    type="date"
                    value={formData.endDate}
                    onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
                    required
                  />

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1.5">
                      Remarks
                    </label>
                    <textarea
                      className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                      rows={4}
                      placeholder="Add any additional remarks..."
                      value={formData.remarks}
                      onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
                    />
                  </div>

                  <Button type="submit" fullWidth className="mt-6">
                    Submit Leave Request
                  </Button>
                </form>
              </Card>

              {/* Leave History */}
              <Card>
                <h2 className="text-xl font-semibold text-gray-800 mb-6">Leave History</h2>
                <div className="space-y-4">
                  {leaveHistory.map((leave) => (
                    <div
                      key={leave.id}
                      className="p-4 bg-gray-50 rounded-lg border border-gray-200"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-semibold text-gray-800">{leave.type}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm ${leave.color}`}>
                          {leave.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">{leave.dates}</p>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
