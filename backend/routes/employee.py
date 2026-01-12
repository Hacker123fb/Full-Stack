from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Employee
from utils.decorators import admin_required
from datetime import datetime

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_all_employees():
    """Get all employees - Admin only"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        department = request.args.get('department')
        search = request.args.get('search')
        
        query = Employee.query
        
        if department:
            query = query.filter(Employee.department == department)
        
        if search:
            query = query.filter(
                db.or_(
                    Employee.first_name.ilike(f'%{search}%'),
                    Employee.last_name.ilike(f'%{search}%'),
                    Employee.employee_code.ilike(f'%{search}%')
                )
            )
        
        employees = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'employees': [emp.to_dict() for emp in employees.items],
            'total': employees.total,
            'pages': employees.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    """Get employee by ID"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        employee = Employee.query.get_or_404(id)
        
        if user.role == 'Employee' and employee.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'employee': employee.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_own_profile():
    """Get logged-in user's employee profile"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee profile not found'}), 404
        
        return jsonify({'employee': employee.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_own_profile():
    """Update own profile - limited fields"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee profile not found'}), 404
        
        data = request.get_json()
        allowed_fields = ['phone', 'address', 'emergency_contact', 'profile_picture']
        
        for field in allowed_fields:
            if field in data:
                setattr(employee, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'employee': employee.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_employee(id):
    """Update employee - Admin can edit all fields"""
    try:
        employee = Employee.query.get_or_404(id)
        data = request.get_json()
        
        editable_fields = [
            'first_name', 'last_name', 'phone', 'date_of_birth', 'gender',
            'address', 'department', 'designation', 'employment_type',
            'profile_picture', 'emergency_contact'
        ]
        
        for field in editable_fields:
            if field in data:
                if field == 'date_of_birth' and data[field]:
                    setattr(employee, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                else:
                    setattr(employee, field, data[field])
        
        if 'role' in data and employee.user:
            employee.user.role = data['role']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Employee updated successfully',
            'employee': employee.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_employee(id):
    """Deactivate employee - Admin only"""
    try:
        employee = Employee.query.get_or_404(id)
        
        if employee.user:
            employee.user.is_active = False
        
        db.session.commit()
        
        return jsonify({'message': 'Employee deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    """Get list of all departments"""
    departments = db.session.query(Employee.department).distinct().all()
    return jsonify({
        'departments': [d[0] for d in departments if d[0]]
    }), 200
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from models import User, Employee, Attendance
from flask import jsonify

# =========================
# ADMIN ROUTES
# =========================



@employee_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def admin_list_users():
    users = User.query.all()
    return jsonify({
        'users': [u.to_dict() for u in users]
    }), 200
@employee_bp.route('/admin/stats', methods=['GET'])
@jwt_required()
@admin_required
def admin_stats():
    return jsonify({
        'total_users': User.query.count(),
        'total_employees': Employee.query.count(),
        'total_attendance_records': Attendance.query.count()
    }), 200
