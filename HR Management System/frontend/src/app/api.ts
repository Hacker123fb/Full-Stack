const API_BASE = 'http://127.0.0.1:5000/api';

export async function apiRequest(
  path: string,
  method: string = 'GET',
  body?: any
) {
  const token = localStorage.getItem('access_token');

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.json();
}

/* ================= AUTH ================= */
export const login = (email: string, password: string) =>
  apiRequest('/auth/login', 'POST', { email, password });

/* ================= ATTENDANCE (EMPLOYEE) ================= */
export const employeeCheckIn = () =>
  apiRequest('/attendance/checkin', 'POST');

export const employeeCheckOut = () =>
  apiRequest('/attendance/checkout', 'POST');

export const getTodayAttendance = () =>
  apiRequest('/attendance/today', 'GET');

export const getMyAttendanceHistory = () =>
  apiRequest('/attendance/my-history', 'GET');

/* ================= ATTENDANCE (HR / ADMIN) ================= */
export const getAllAttendance = (date?: string) =>
  apiRequest(`/attendance/all${date ? `?date=${date}` : ''}`, 'GET');

/* ================= LEAVE (HR) ================= */
export const getAllLeaveRequests = () =>
  apiRequest('/leaves/all', 'GET');

export const approveLeave = (employee_id: number, date?: string) =>
  apiRequest('/attendance/manual', 'POST', {
    employee_id,
    date: date || new Date().toISOString().slice(0, 10),
    status: 'Present',
  });

export const rejectLeave = (employee_id: number, date?: string) =>
  apiRequest('/attendance/manual', 'POST', {
    employee_id,
    date: date || new Date().toISOString().slice(0, 10),
    status: 'Absent',
  });
// ===== ADMIN APIs =====
export const getAdminStats = () =>
  apiRequest('/employees/admin/stats', 'GET');

export const getAllUsers = () =>
  apiRequest('/employees/admin/users', 'GET');

