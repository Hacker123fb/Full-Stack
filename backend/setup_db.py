"""
Database Setup Script - Fixed Version
Run: python setup_db.py
"""
from app import create_app
from models import db, User, Employee, Payroll
from datetime import date

app = create_app()

with app.app_context():
    # Drop all tables and recreate (clean start)
    db.drop_all()
    db.create_all()
    print("✅ Database tables created (fresh)!")
    
    # ==================== CREATE ADMIN ====================
    admin = User(email='admin@company.com', role='Admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    admin_emp = Employee(
        user_id=admin.id,
        employee_code='EMP00001',
        first_name='Admin',
        last_name='User',
        department='Administration',
        designation='System Administrator',
        date_of_joining=date(2020, 1, 1)
    )
    db.session.add(admin_emp)
    db.session.commit()
    print("✅ Admin user created!")
    
    # ==================== CREATE HR ====================
    hr = User(email='hr@company.com', role='HR')
    hr.set_password('hr123')
    db.session.add(hr)
    db.session.commit()
    
    hr_emp = Employee(
        user_id=hr.id,
        employee_code='EMP00002',
        first_name='HR',
        last_name='Manager',
        department='Human Resources',
        designation='HR Manager',
        date_of_joining=date(2021, 6, 1)
    )
    db.session.add(hr_emp)
    db.session.commit()
    print("✅ HR user created!")
    
    # ==================== CREATE EMPLOYEE ====================
    emp = User(email='employee@company.com', role='Employee')
    emp.set_password('emp123')
    db.session.add(emp)
    db.session.commit()
    
    emp_profile = Employee(
        user_id=emp.id,
        employee_code='EMP00003',
        first_name='John',
        last_name='Doe',
        phone='9876543210',
        department='Engineering',
        designation='Software Developer',
        date_of_joining=date(2023, 1, 15)
    )
    db.session.add(emp_profile)
    db.session.commit()
    print("✅ Sample employee created!")
    
    # ==================== CREATE SAMPLE PAYROLL ====================
    payroll = Payroll(
        employee_id=3,
        month=1,
        year=2025,
        basic_salary=50000,
        hra=10000,
        da=5000,
        ta=3000,
        pf_deduction=6000,
        tax_deduction=5000
    )
    payroll.calculate_salary()
    db.session.add(payroll)
    db.session.commit()
    print("✅ Sample payroll created!")
    
    # ==================== SUMMARY ====================
    print("\n" + "="*50)
    print("🎉 DATABASE SETUP COMPLETE!")
    print("="*50)
    print("\n📧 Login Credentials:")
    print("-"*30)
    print("👤 Admin:    admin@company.com / admin123")
    print("👤 HR:       hr@company.com / hr123")
    print("👤 Employee: employee@company.com / emp123")
    print("-"*30)
    
    # Verify data
    print("\n📊 Database Summary:")
    print(f"   Users: {User.query.count()}")
    print(f"   Employees: {Employee.query.count()}")
    print(f"   Payrolls: {Payroll.query.count()}")