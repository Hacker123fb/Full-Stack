from . import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    address = db.Column(db.Text)
    department = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    date_of_joining = db.Column(db.Date, nullable=False)
    employment_type = db.Column(db.Enum('Full-time', 'Part-time', 'Contract'), default='Full-time')
    profile_picture = db.Column(db.String(255))
    emergency_contact = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True,
                                     foreign_keys='LeaveRequest.employee_id')
    payrolls = db.relationship('Payroll', backref='employee', lazy=True)
    notifications = db.relationship('Notification', backref='employee', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employee_code': self.employee_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'email': self.user.email if self.user else None,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'address': self.address,
            'department': self.department,
            'designation': self.designation,
            'date_of_joining': self.date_of_joining.isoformat() if self.date_of_joining else None,
            'employment_type': self.employment_type,
            'profile_picture': self.profile_picture,
            'emergency_contact': self.emergency_contact,
            'role': self.user.role if self.user else None
        }