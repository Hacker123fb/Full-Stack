import React from 'react';
import { User } from 'lucide-react';

interface HeaderProps {
  userName: string;
  userRole: string;
}

export function Header({ userName, userRole }: HeaderProps) {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
      <div>
        <h2 className="text-xl font-semibold text-gray-800">
          Welcome back, {userName}!
        </h2>
        <p className="text-sm text-gray-500">{userRole}</p>
      </div>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center">
          <User className="text-indigo-600" size={20} />
        </div>
      </div>
    </header>
  );
}
