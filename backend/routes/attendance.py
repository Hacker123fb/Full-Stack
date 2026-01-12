from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Employee, Attendance
from utils.decorators import admin_required
from datetime import datetime, date, timedelta

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/checkin', methods=['POST'])
@jwt_required()
def check_in():
    """Mark attendance check-in"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        today = date.today()
        
        existing = Attendance.query.filter_by(
            employee_id=employee.id,
            date=today
        ).first()
        
        if existing and existing.check_in:
            return jsonify({'error': 'Already checked in today'}), 400
        
        if existing:
            existing.check_in = datetime.now().time()
            existing.status = 'Present'
        else:
            existing = Attendance(
                employee_id=employee.id,
                date=today,
                check_in=datetime.now().time(),
                status='Present'
            )
            db.session.add(existing)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in successful',
            'attendance': existing.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/checkout', methods=['POST'])
@jwt_required()
def check_out():
    """Mark attendance check-out"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        today = date.today()
        
        attendance = Attendance.query.filter_by(
            employee_id=employee.id,
            date=today
        ).first()
        
        if not attendance or not attendance.check_in:
            return jsonify({'error': 'No check-in found for today'}), 400
        
        if attendance.check_out:
            return jsonify({'error': 'Already checked out today'}), 400
        
        attendance.check_out = datetime.now().time()
        attendance.calculate_work_hours()
        
        if attendance.work_hours and attendance.work_hours < 4:
            attendance.status = 'Half-day'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Check-out successful',
            'attendance': attendance.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/today', methods=['GET'])
@jwt_required()
def get_today_attendance():
    """Get today's attendance for logged-in user"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        attendance = Attendance.query.filter_by(
            employee_id=employee.id,
            date=date.today()
        ).first()
        
        return jsonify({
            'attendance': attendance.to_dict() if attendance else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/my-history', methods=['GET'])
@jwt_required()
def get_my_attendance_history():
    """Get attendance history for logged-in user"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Attendance.query.filter_by(employee_id=employee.id)
        
        if start_date:
            query = query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        if not start_date and not end_date:
            thirty_days_ago = date.today() - timedelta(days=30)
            query = query.filter(Attendance.date >= thirty_days_ago)
        
        attendances = query.order_by(Attendance.date.desc()).all()
        
        return jsonify({
            'attendances': [att.to_dict() for att in attendances]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/weekly-summary', methods=['GET'])
@jwt_required()
def get_weekly_summary():
    """Get weekly attendance summary"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        attendances = Attendance.query.filter(
            Attendance.employee_id == employee.id,
            Attendance.date >= week_start,
            Attendance.date <= week_end
        ).all()
        
        summary = {
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'total_days': len(attendances),
            'present': sum(1 for a in attendances if a.status == 'Present'),
            'absent': sum(1 for a in attendances if a.status == 'Absent'),
            'half_days': sum(1 for a in attendances if a.status == 'Half-day'),
            'leaves': sum(1 for a in attendances if a.status == 'Leave'),
            'total_hours': sum(float(a.work_hours or 0) for a in attendances),
            'daily_records': [att.to_dict() for att in attendances]
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/all', methods=['GET'])
@jwt_required()
@admin_required
def get_all_attendance():
    """Get all employees attendance - Admin only"""
    try:
        date_str = request.args.get('date', date.today().isoformat())
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        department = request.args.get('department')
        
        query = Attendance.query.filter_by(date=query_date)
        
        if department:
            query = query.join(Employee).filter(Employee.department == department)
        
        attendances = query.all()
        
        return jsonify({
            'date': date_str,
            'attendances': [att.to_dict() for att in attendances],
            'summary': {
                'total': len(attendances),
                'present': sum(1 for a in attendances if a.status == 'Present'),
                'absent': sum(1 for a in attendances if a.status == 'Absent'),
                'on_leave': sum(1 for a in attendances if a.status == 'Leave')
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attendance_bp.route('/manual', methods=['POST'])
@jwt_required()
@admin_required
def manual_attendance():
    """Manual attendance entry - Admin only"""
    try:
        data = request.get_json()
        
        required = ['employee_id', 'date', 'status']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        att_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        existing = Attendance.query.filter_by(
            employee_id=data['employee_id'],
            date=att_date
        ).first()
        
        if existing:
            existing.status = data['status']
            existing.notes = data.get('notes')
            if data.get('check_in'):
                existing.check_in = datetime.strptime(data['check_in'], '%H:%M').time()
            if data.get('check_out'):
                existing.check_out = datetime.strptime(data['check_out'], '%H:%M').time()
                existing.calculate_work_hours()
        else:
            existing = Attendance(
                employee_id=data['employee_id'],
                date=att_date,
                status=data['status'],
                notes=data.get('notes')
            )
            if data.get('check_in'):
                existing.check_in = datetime.strptime(data['check_in'], '%H:%M').time()
            if data.get('check_out'):
                existing.check_out = datetime.strptime(data['check_out'], '%H:%M').time()
                existing.calculate_work_hours()
            db.session.add(existing)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Attendance recorded successfully',
            'attendance': existing.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500