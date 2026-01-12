from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Employee, Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get logged-in user's notifications"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = request.args.get('limit', 50, type=int)
        
        query = Notification.query.filter_by(employee_id=employee.id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        notifications = query.order_by(Notification.created_at.desc())\
            .limit(limit).all()
        
        unread_count = Notification.query.filter_by(
            employee_id=employee.id,
            is_read=False
        ).count()
        
        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(id):
    """Mark notification as read"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        notification = Notification.query.get_or_404(id)
        
        if notification.employee_id != employee.id:
            return jsonify({'error': 'Access denied'}), 403
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications as read"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        Notification.query.filter_by(
            employee_id=employee.id,
            is_read=False
        ).update({'is_read': True})
        
        db.session.commit()
        
        return jsonify({'message': 'All notifications marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_notification(id):
    """Delete notification"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        notification = Notification.query.get_or_404(id)
        
        if notification.employee_id != employee.id:
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({'message': 'Notification deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500