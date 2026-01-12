from . import db
from datetime import datetime

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(
        db.Enum('Casual', 'Sick', 'Earned', 'Maternity', 'Paternity', 'Unpaid'),
        nullable=False
    )
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum('Pending', 'Approved', 'Rejected', 'Cancelled'),
        default='Pending'
    )
    reviewed_by = db.Column(db.Integer, db.ForeignKey('employees.id'))
    review_comment = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship for reviewer
    reviewer = db.relationship('Employee', foreign_keys=[reviewed_by], backref='reviewed_leaves')
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.first_name + ' ' + self.employee.last_name if self.employee else None,
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'total_days': self.total_days,
            'reason': self.reason,
            'status': self.status,
            'reviewed_by': self.reviewed_by,
            'reviewer_name': self.reviewer.first_name + ' ' + self.reviewer.last_name if self.reviewer else None,
            'review_comment': self.review_comment,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }