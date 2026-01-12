import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiRequest } from '../api';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { Card } from '../components/Card';

export function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    console.log('LOGIN CLICKED'); // 🔥 MUST PRINT
    setLoading(true);

    try {
      const data = await apiRequest('/auth/login', 'POST', {
        email,
        password,
      });

      console.log('LOGIN RESPONSE:', data);

      if (!data?.access_token || !data?.user) {
        alert('Invalid login response');
        return;
      }

      // ✅ STORE TOKENS
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);

      // ✅ STORE USER INFO
      localStorage.setItem('userRole', data.user.role);

      if (data.employee) {
        localStorage.setItem(
          'userName',
          `${data.employee.first_name} ${data.employee.last_name}`
        );
      } else {
        localStorage.setItem('userName', 'User');
      }

      console.log('LOCALSTORAGE AFTER LOGIN:', {
        role: localStorage.getItem('userRole'),
        token: localStorage.getItem('access_token'),
      });

      // ✅ ROLE-BASED REDIRECT
      const role = data.user.role;

      if (role === 'Admin') {
        navigate('/admin-dashboard', { replace: true });
      } else if (role === 'HR') {
        navigate('/hr-dashboard', { replace: true });
      } else {
        navigate('/dashboard', { replace: true });
      }

    } catch (err: any) {
      console.error('LOGIN ERROR:', err);
      alert(err?.error || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-indigo-600 mb-2">Dayflow</h1>
          <p className="text-gray-600">HR Management System</p>
        </div>

        <h2 className="text-2xl font-semibold text-gray-800 mb-6">Login</h2>

        {/* ❌ NO FORM SUBMIT */}
        <div className="space-y-4">
          <Input
            label="Email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            fullWidth
            className="mt-6"
            onClick={handleLogin}
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </Button>
        </div>

        <p className="text-center mt-6 text-gray-600">
          Don&apos;t have an account?{' '}
          <Link
            to="/signup"
            className="text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Sign Up
          </Link>
        </p>
      </Card>
    </div>
  );
}
