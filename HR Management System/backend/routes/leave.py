from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Employee, LeaveRequest, Attendance
from utils.decorators import admin_required
from utils.helpers import create_notification
from datetime import datetime, timedelta

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_leave():
    """Apply for leave"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        data = request.get_json()
        
        required = ['leave_type', 'start_date', 'end_date', 'reason']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        if end_date < start_date:
            return jsonify({'error': 'End date cannot be before start date'}), 400
        
        total_days = (end_date - start_date).days + 1
        
        overlapping = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee.id,
            LeaveRequest.status.in_(['Pending', 'Approved']),
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date
        ).first()
        
        if overlapping:
            return jsonify({'error': 'Leave dates overlap with existing request'}), 400
        
        leave = LeaveRequest(
            employee_id=employee.id,
            leave_type=data['leave_type'],
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            reason=data['reason']
        )
        
        db.session.add(leave)
        db.session.commit()
        
        return jsonify({
            'message': 'Leave application submitted successfully',
            'leave': leave.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/my-leaves', methods=['GET'])
@jwt_required()
def get_my_leaves():
    """Get logged-in user's leave requests"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        status = request.args.get('status')
        
        query = LeaveRequest.query.filter_by(employee_id=employee.id)
        
        if status:
            query = query.filter_by(status=status)
        
        leaves = query.order_by(LeaveRequest.created_at.desc()).all()
        
        return jsonify({
            'leaves': [leave.to_dict() for leave in leaves]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_leave(id):
    """Get leave request by ID"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        leave = LeaveRequest.query.get_or_404(id)
        
        if user.role == 'Employee':
            employee = Employee.query.filter_by(user_id=user_id).first()
            if leave.employee_id != employee.id:
                return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'leave': leave.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/<int:id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_leave(id):
    """Cancel own leave request"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        leave = LeaveRequest.query.get_or_404(id)
        
        if leave.employee_id != employee.id:
            return jsonify({'error': 'Access denied'}), 403
        
        if leave.status != 'Pending':
            return jsonify({'error': 'Can only cancel pending requests'}), 400
        
        leave.status = 'Cancelled'
        db.session.commit()
        
        return jsonify({
            'message': 'Leave request cancelled',
            'leave': leave.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/pending', methods=['GET'])
@jwt_required()
@admin_required
def get_pending_leaves():
    """Get all pending leave requests - Admin only"""
    try:
        leaves = LeaveRequest.query.filter_by(status='Pending')\
            .order_by(LeaveRequest.created_at.asc()).all()
        
        return jsonify({
            'leaves': [leave.to_dict() for leave in leaves]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/all', methods=['GET'])
@jwt_required()
@admin_required
def get_all_leaves():
    """Get all leave requests - Admin only"""
    try:
        status = request.args.get('status')
        department = request.args.get('department')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = LeaveRequest.query
        
        if status:
            query = query.filter_by(status=status)
        
        if department:
            query = query.join(Employee).filter(Employee.department == department)
        
        leaves = query.order_by(LeaveRequest.created_at.desc())\
            .paginate(page=page, per_page=per_page)
        
        return jsonify({
            'leaves': [leave.to_dict() for leave in leaves.items],
            'total': leaves.total,
            'pages': leaves.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/<int:id>/review', methods=['PUT'])
@jwt_required()
@admin_required
def review_leave(id):
    """Approve or reject leave - Admin only"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        admin_employee = Employee.query.filter_by(user_id=user_id).first()
        
        leave = LeaveRequest.query.get_or_404(id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        if data['status'] not in ['Approved', 'Rejected']:
            return jsonify({'error': 'Invalid status'}), 400
        
        if leave.status != 'Pending':
            return jsonify({'error': 'Can only review pending requests'}), 400
        
        leave.status = data['status']
        leave.review_comment = data.get('comment')
        leave.reviewed_by = admin_employee.id if admin_employee else None
        leave.reviewed_at = datetime.utcnow()
        
        if data['status'] == 'Approved':
            current_date = leave.start_date
            while current_date <= leave.end_date:
                attendance = Attendance.query.filter_by(
                    employee_id=leave.employee_id,
                    date=current_date
                ).first()
                
                if attendance:
                    attendance.status = 'Leave'
                else:
                    attendance = Attendance(
                        employee_id=leave.employee_id,
                        date=current_date,
                        status='Leave'
                    )
                    db.session.add(attendance)
                
                current_date += timedelta(days=1)
        
        create_notification(
            employee_id=leave.employee_id,
            title=f'Leave {data["status"]}',
            message=f'Your {leave.leave_type} leave from {leave.start_date} to {leave.end_date} has been {data["status"].lower()}.',
            notification_type='Leave',
            reference_id=leave.id,
            reference_type='leave_requests'
        )
        
        db.session.commit()
        
        return jsonify({
            'message': f'Leave {data["status"].lower()} successfully',
            'leave': leave.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leave_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_leave_balance():
    """Get leave balance for current user"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        leave_quotas = {
            'Casual': 12,
            'Sick': 12,
            'Earned': 15,
            'Maternity': 180,
            'Paternity': 15,
            'Unpaid': 999
        }
        
        current_year = datetime.now().year
        approved_leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee.id,
            LeaveRequest.status == 'Approved',
            db.extract('year', LeaveRequest.start_date) == current_year
        ).all()
        
        used_leaves = {}
        for leave in approved_leaves:
            leave_type = leave.leave_type
            used_leaves[leave_type] = used_leaves.get(leave_type, 0) + leave.total_days
        
        balance = {}
        for leave_type, quota in leave_quotas.items():
            used = used_leaves.get(leave_type, 0)
            balance[leave_type] = {
                'total': quota if quota != 999 else 'Unlimited',
                'used': used,
                'remaining': (quota - used) if quota != 999 else 'Unlimited'
            }
        
        return jsonify({'balance': balance}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500