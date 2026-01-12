import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { User, Calendar, FileText, DollarSign, Clock, CircleCheck } from 'lucide-react';
import { apiRequest } from '../api';

export function EmployeeDashboard() {
  const navigate = useNavigate();
  const [employee, setEmployee] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const userName =
    employee ? `${employee.first_name} ${employee.last_name}` : 'User';

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const quickActions = [
    { icon: User, label: 'My Profile', color: 'bg-blue-500', path: '/profile' },
    { icon: Calendar, label: 'Attendance', color: 'bg-green-500', path: '/attendance' },
    { icon: FileText, label: 'Leave Requests', color: 'bg-purple-500', path: '/leave' },
    { icon: DollarSign, label: 'Payroll', color: 'bg-orange-500', path: '/profile' },
  ];

  const recentActivity = [
    { action: 'Checked in', time: 'Today at 9:00 AM', icon: CircleCheck, color: 'text-green-600' },
    { action: 'Leave request approved', time: 'Yesterday', icon: CircleCheck, color: 'text-green-600' },
    { action: 'Checked out', time: 'Yesterday at 6:00 PM', icon: Clock, color: 'text-gray-600' },
  ];

 useEffect(() => {
  const fetchMe = async () => {
    try {
      const data = await apiRequest('/auth/me');

      console.log('ME RESPONSE:', data); // debug (optional)

      if (data && data.employee) {
        setEmployee(data.employee);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false); // ✅ THIS WAS MISSING
    }
  };

  fetchMe();
}, []);



  if (loading) {
    return <div className="p-6">Loading dashboard...</div>;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole="employee" onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName={userName} userRole="Employee" />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {quickActions.map((action, index) => (
                <Card
                  key={index}
                  onClick={() => navigate(action.path)}
                  className="cursor-pointer hover:scale-105 transition-transform"
                >
                  <div className="flex items-center gap-4">
                    <div className={`${action.color} p-3 rounded-lg`}>
                      <action.icon className="text-white" size={24} />
                    </div>
                    <div>
                      <p className="text-gray-500 text-sm">Quick Access</p>
                      <h3 className="font-semibold text-gray-800">{action.label}</h3>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            <Card>
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-center gap-4 pb-4 border-b border-gray-100 last:border-0">
                    <activity.icon className={activity.color} size={20} />
                    <div className="flex-1">
                      <p className="font-medium text-gray-800">{activity.action}</p>
                      <p className="text-sm text-gray-500">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}
