from datetime import datetime, date
from models import db, Notification

def create_notification(employee_id, title, message, notification_type='General', 
                       reference_id=None, reference_type=None):
    """Helper to create notifications"""
    notification = Notification(
        employee_id=employee_id,
        title=title,
        message=message,
        type=notification_type,
        reference_id=reference_id,
        reference_type=reference_type
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def calculate_business_days(start_date, end_date):
    """Calculate number of business days between two dates"""
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday to Friday
            days += 1
        current = current + timedelta(days=1)
    return days

def generate_employee_code():
    """Generate unique employee code"""
    from models import Employee
    last_emp = Employee.query.order_by(Employee.id.desc()).first()
    if last_emp:
        last_num = int(last_emp.employee_code.replace('EMP', ''))
        return f"EMP{str(last_num + 1).zfill(5)}"
    return "EMP00001"