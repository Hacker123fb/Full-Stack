"""
API Testing Script
Run: python test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_response(name, response):
    status = response.status_code
    if 200 <= status < 300:
        color = Colors.GREEN
        symbol = "✅"
    else:
        color = Colors.RED
        symbol = "❌"
    
    print(f"\n{symbol} {color}{name}{Colors.END}")
    print(f"   Status: {status}")
    try:
        print(f"   Response: {json.dumps(response.json(), indent=2)[:500]}")
    except:
        print(f"   Response: {response.text[:200]}")

def test_apis():
    print("="*60)
    print("🧪 EMPLOYEE MANAGEMENT API TESTING")
    print("="*60)
    
    # ==================== HEALTH CHECK ====================
    print(f"\n{Colors.BLUE}━━━ HEALTH CHECK ━━━{Colors.END}")
    
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    # ==================== AUTH TESTS ====================
    print(f"\n{Colors.BLUE}━━━ AUTHENTICATION ━━━{Colors.END}")
    
    # Test Login with Admin
    login_data = {
        "email": "admin@company.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("Admin Login", response)
    
    if response.status_code == 200:
        admin_token = response.json()['access_token']
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
    else:
        print(f"{Colors.RED}❌ Cannot proceed without admin token{Colors.END}")
        return
    
    # Test Login with Employee
    login_data = {
        "email": "employee@company.com",
        "password": "emp123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("Employee Login", response)
    
    if response.status_code == 200:
        emp_token = response.json()['access_token']
        emp_headers = {"Authorization": f"Bearer {emp_token}"}
    else:
        emp_headers = admin_headers
    
    # Get Current User
    response = requests.get(f"{BASE_URL}/auth/me", headers=admin_headers)
    print_response("Get Current User", response)
    
    # ==================== EMPLOYEE TESTS ====================
    print(f"\n{Colors.BLUE}━━━ EMPLOYEES ━━━{Colors.END}")
    
    # Get All Employees (Admin)
    response = requests.get(f"{BASE_URL}/employees/", headers=admin_headers)
    print_response("Get All Employees", response)
    
    # Get Own Profile
    response = requests.get(f"{BASE_URL}/employees/profile", headers=emp_headers)
    print_response("Get Own Profile", response)
    
    # Update Own Profile
    update_data = {
        "phone": "9999888877",
        "address": "123 Test Street"
    }
    response = requests.put(f"{BASE_URL}/employees/profile", headers=emp_headers, json=update_data)
    print_response("Update Own Profile", response)
    
    # Get Departments
    response = requests.get(f"{BASE_URL}/employees/departments", headers=emp_headers)
    print_response("Get Departments", response)
    
    # ==================== ATTENDANCE TESTS ====================
    print(f"\n{Colors.BLUE}━━━ ATTENDANCE ━━━{Colors.END}")
    
    # Check-In
    response = requests.post(f"{BASE_URL}/attendance/check-in", headers=emp_headers)
    print_response("Check-In", response)
    
    # Get Today's Attendance
    response = requests.get(f"{BASE_URL}/attendance/today", headers=emp_headers)
    print_response("Today's Attendance", response)
    
    # Check-Out
    response = requests.post(f"{BASE_URL}/attendance/check-out", headers=emp_headers)
    print_response("Check-Out", response)
    
    # Get My History
    response = requests.get(f"{BASE_URL}/attendance/my-history", headers=emp_headers)
    print_response("My Attendance History", response)
    
    # Get Weekly Summary
    response = requests.get(f"{BASE_URL}/attendance/weekly-summary", headers=emp_headers)
    print_response("Weekly Summary", response)
    
    # Get All Attendance (Admin)
    response = requests.get(f"{BASE_URL}/attendance/all", headers=admin_headers)
    print_response("All Attendance (Admin)", response)
    
    # ==================== LEAVE TESTS ====================
    print(f"\n{Colors.BLUE}━━━ LEAVES ━━━{Colors.END}")
    
    # Apply Leave
    leave_data = {
        "leave_type": "Casual",
        "start_date": "2025-02-01",
        "end_date": "2025-02-03",
        "reason": "Personal work - Testing API"
    }
    response = requests.post(f"{BASE_URL}/leaves/apply", headers=emp_headers, json=leave_data)
    print_response("Apply Leave", response)
    
    leave_id = None
    if response.status_code == 201:
        leave_id = response.json()['leave']['id']
    
    # Get My Leaves
    response = requests.get(f"{BASE_URL}/leaves/my-leaves", headers=emp_headers)
    print_response("My Leaves", response)
    
    # Get Leave Balance
    response = requests.get(f"{BASE_URL}/leaves/balance", headers=emp_headers)
    print_response("Leave Balance", response)
    
    # Get Pending Leaves (Admin)
    response = requests.get(f"{BASE_URL}/leaves/pending", headers=admin_headers)
    print_response("Pending Leaves (Admin)", response)
    
    # Approve Leave (Admin)
    if leave_id:
        approve_data = {
            "status": "Approved",
            "comment": "Approved via API test"
        }
        response = requests.put(f"{BASE_URL}/leaves/{leave_id}/review", headers=admin_headers, json=approve_data)
        print_response("Approve Leave (Admin)", response)
    
    # ==================== PAYROLL TESTS ====================
    print(f"\n{Colors.BLUE}━━━ PAYROLL ━━━{Colors.END}")
    
    # Create Payroll (Admin)
    payroll_data = {
        "employee_id": 3,
        "month": 1,
        "year": 2025,
        "basic_salary": 50000,
        "hra": 10000,
        "da": 5000,
        "ta": 3000,
        "pf_deduction": 6000,
        "tax_deduction": 5000
    }
    response = requests.post(f"{BASE_URL}/payroll/", headers=admin_headers, json=payroll_data)
    print_response("Create Payroll (Admin)", response)
    
    # Get My Payroll
    response = requests.get(f"{BASE_URL}/payroll/my-payroll", headers=emp_headers)
    print_response("My Payroll", response)
    
    # Get All Payroll (Admin)
    response = requests.get(f"{BASE_URL}/payroll/all?year=2025", headers=admin_headers)
    print_response("All Payroll (Admin)", response)
    
    # ==================== NOTIFICATION TESTS ====================
    print(f"\n{Colors.BLUE}━━━ NOTIFICATIONS ━━━{Colors.END}")
    
    # Get Notifications
    response = requests.get(f"{BASE_URL}/notifications/", headers=emp_headers)
    print_response("Get Notifications", response)
    
    # Mark All as Read
    response = requests.put(f"{BASE_URL}/notifications/read-all", headers=emp_headers)
    print_response("Mark All as Read", response)
    
    # ==================== SUMMARY ====================
    print("\n" + "="*60)
    print(f"{Colors.GREEN}🎉 API TESTING COMPLETE!{Colors.END}")
    print("="*60)

if __name__ == "__main__":
    print("\n⚠️  Make sure Flask server is running: python app.py\n")
    try:
        test_apis()
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Cannot connect to server!{Colors.END}")
        print("   Run: python app.py")