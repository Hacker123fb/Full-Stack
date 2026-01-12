import React from 'react';
import { Link } from 'react-router-dom';

type UserRole = 'employee' | 'admin' | 'hr';

interface SidebarProps {
  userRole: UserRole;
  onLogout: () => void;
}

export function Sidebar({ userRole, onLogout }: SidebarProps) {
  return (
    <aside className="w-64 bg-white border-r p-4">
      <h2 className="text-xl font-bold mb-6">Dayflow</h2>

      <nav className="space-y-3">
        {userRole === 'employee' && (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/employee-attendance">Attendance</Link>
            <Link to="/leave">Leave</Link>
          </>
        )}

        {userRole === 'hr' && (
          <>
            <Link to="/hr-dashboard">HR Dashboard</Link>
            <Link to="/hr-attendance">Attendance Control</Link>
          </>
        )}

        {userRole === 'admin' && (
          <>
            <Link to="/admin-dashboard">Admin Dashboard</Link>
          </>
        )}
      </nav>

      <button
        onClick={onLogout}
        className="mt-10 text-red-600 font-semibold"
      >
        Logout
      </button>
    </aside>
  );
}
