from . import db
from datetime import datetime, date

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    status = db.Column(
        db.Enum('Present', 'Absent', 'Half-day', 'Leave', 'Holiday', 'Weekend'),
        default='Present'
    )
    work_hours = db.Column(db.Numeric(4, 2))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one record per employee per day
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'date', name='unique_employee_date'),
    )
    
    def calculate_work_hours(self):
        if self.check_in and self.check_out:
            check_in_dt = datetime.combine(self.date, self.check_in)
            check_out_dt = datetime.combine(self.date, self.check_out)
            diff = check_out_dt - check_in_dt
            self.work_hours = round(diff.total_seconds() / 3600, 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.first_name + ' ' + self.employee.last_name if self.employee else None,
            'date': self.date.isoformat() if self.date else None,
            'check_in': self.check_in.strftime('%H:%M:%S') if self.check_in else None,
            'check_out': self.check_out.strftime('%H:%M:%S') if self.check_out else None,
            'status': self.status,
            'work_hours': float(self.work_hours) if self.work_hours else None,
            'notes': self.notes
        }