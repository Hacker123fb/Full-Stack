from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity
)
from models import db, User, Employee
from utils.helpers import generate_employee_code
from datetime import datetime
from flask_cors import cross_origin
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user and create employee profile"""
    try:
        data = request.get_json()
        
        required = ['email', 'password', 'first_name', 'last_name', 'date_of_joining']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        user = User(
            email=data['email'],
            role=data.get('role', 'Employee')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        
        employee = Employee(
            user_id=user.id,
            employee_code=generate_employee_code(),
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            address=data.get('address'),
            department=data.get('department'),
            designation=data.get('designation'),
            date_of_joining=datetime.strptime(data['date_of_joining'], '%Y-%m-%d').date(),
            employment_type=data.get('employment_type', 'Full-time')
        )
        db.session.add(employee)
        db.session.commit()
        
        # ✅ FIX: Convert user.id to string
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict(),
            'employee': employee.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # ✅ FIX: Convert user.id to string
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        employee = Employee.query.filter_by(user_id=user.id).first()
        print("LOGIN API HIT")

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'employee': employee.to_dict() if employee else None,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    # ✅ user_id is already string from token
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user details"""
    # ✅ FIX: Convert string back to int for database query
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    employee = Employee.query.filter_by(user_id=user.id).first()
    
    return jsonify({
        'user': user.to_dict(),
        'employee': employee.to_dict() if employee else None
    }), 200

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        # ✅ FIX: Convert string back to int
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        data = request.get_json()
        
        if not user.check_password(data.get('current_password', '')):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        if len(data.get('new_password', '')) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500