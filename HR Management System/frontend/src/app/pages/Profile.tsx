import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Card } from '../components/Card';
import { User, Mail, Phone, MapPin, Briefcase, Calendar, DollarSign } from 'lucide-react';
import { apiRequest } from '../api';

export function Profile() {
  const navigate = useNavigate();
  const userName = localStorage.getItem('userName') || 'User';
  const userRole = (localStorage.getItem('userRole') as 'employee' | 'admin') || 'employee';   const [profile, setProfile] = useState<any>(null);
  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const profileData = {
    name: userName,
    email: 'john.doe@dayflow.com',
    phone: '+1 (555) 123-4567',
    address: '123 Main Street, New York, NY 10001',
    employeeId: 'EMP-001',
    department: 'Engineering',
    position: 'Software Engineer',
    joinDate: 'January 15, 2023',
    salary: '$85,000',
  };
  useEffect(() => {
  const fetchProfile = async () => {
    const data = await apiRequest('/employees/me');
    setProfile(data);
  };

  fetchProfile();
}, []);


  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar userRole={userRole} onLogout={handleLogout} />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header userName={userName} userRole={userRole === 'admin' ? 'Administrator' : 'Employee'} />

        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">My Profile</h1>

            {/* Profile Picture and Basic Info */}
            <Card className="mb-8">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 bg-indigo-100 rounded-full flex items-center justify-center">
                  <User className="text-indigo-600" size={48} />
                </div>
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800">{profileData.name}</h2>
                  <p className="text-gray-600">{profileData.position}</p>
                  <p className="text-sm text-gray-500">{profileData.employeeId}</p>
                </div>
              </div>
            </Card>

            {/* Personal Details */}
            <Card className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">Personal Details</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center gap-3">
                  <Mail className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Email</p>
                    <p className="text-gray-800">{profileData.email}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Phone className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Phone</p>
                    <p className="text-gray-800">{profileData.phone}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 md:col-span-2">
                  <MapPin className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Address</p>
                    <p className="text-gray-800">{profileData.address}</p>
                  </div>
                </div>
              </div>
            </Card>

            {/* Job Details */}
            <Card className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">Job Details</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center gap-3">
                  <Briefcase className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Department</p>
                    <p className="text-gray-800">{profileData.department}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <User className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Position</p>
                    <p className="text-gray-800">{profileData.position}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Calendar className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Join Date</p>
                    <p className="text-gray-800">{profileData.joinDate}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <DollarSign className="text-gray-400" size={20} />
                  <div>
                    <p className="text-sm text-gray-500">Salary (Annual)</p>
                    <p className="text-gray-800">{profileData.salary}</p>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}
