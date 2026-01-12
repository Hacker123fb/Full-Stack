from . import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(
        db.Enum('Leave', 'Payroll', 'Attendance', 'General'),
        default='General'
    )
    is_read = db.Column(db.Boolean, default=False)
    reference_id = db.Column(db.Integer)  # ID of related record
    reference_type = db.Column(db.String(50))  # Table name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'reference_id': self.reference_id,
            'reference_type': self.reference_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }