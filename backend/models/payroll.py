from . import db
from datetime import datetime

class Payroll(db.Model):
    __tablename__ = 'payroll'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Numeric(12, 2), nullable=False)
    hra = db.Column(db.Numeric(10, 2), default=0)  # House Rent Allowance
    da = db.Column(db.Numeric(10, 2), default=0)   # Dearness Allowance
    ta = db.Column(db.Numeric(10, 2), default=0)   # Travel Allowance
    other_allowances = db.Column(db.Numeric(10, 2), default=0)
    gross_salary = db.Column(db.Numeric(12, 2))
    pf_deduction = db.Column(db.Numeric(10, 2), default=0)      # Provident Fund
    tax_deduction = db.Column(db.Numeric(10, 2), default=0)
    other_deductions = db.Column(db.Numeric(10, 2), default=0)
    total_deductions = db.Column(db.Numeric(12, 2))
    net_salary = db.Column(db.Numeric(12, 2))
    payment_status = db.Column(
        db.Enum('Pending', 'Processed', 'Paid'),
        default='Pending'
    )
    payment_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one payroll per employee per month
    __table_args__ = (
        db.UniqueConstraint('employee_id', 'month', 'year', name='unique_employee_month_year'),
    )
    
    def calculate_salary(self):
        self.gross_salary = (
            float(self.basic_salary or 0) +
            float(self.hra or 0) +
            float(self.da or 0) +
            float(self.ta or 0) +
            float(self.other_allowances or 0)
        )
        self.total_deductions = (
            float(self.pf_deduction or 0) +
            float(self.tax_deduction or 0) +
            float(self.other_deductions or 0)
        )
        self.net_salary = self.gross_salary - self.total_deductions
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.first_name + ' ' + self.employee.last_name if self.employee else None,
            'month': self.month,
            'year': self.year,
            'basic_salary': float(self.basic_salary) if self.basic_salary else 0,
            'hra': float(self.hra) if self.hra else 0,
            'da': float(self.da) if self.da else 0,
            'ta': float(self.ta) if self.ta else 0,
            'other_allowances': float(self.other_allowances) if self.other_allowances else 0,
            'gross_salary': float(self.gross_salary) if self.gross_salary else 0,
            'pf_deduction': float(self.pf_deduction) if self.pf_deduction else 0,
            'tax_deduction': float(self.tax_deduction) if self.tax_deduction else 0,
            'other_deductions': float(self.other_deductions) if self.other_deductions else 0,
            'total_deductions': float(self.total_deductions) if self.total_deductions else 0,
            'net_salary': float(self.net_salary) if self.net_salary else 0,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        }