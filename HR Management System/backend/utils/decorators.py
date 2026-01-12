from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            try:
                user_id = int(get_jwt_identity())
            except Exception:
                return jsonify({'error': 'Invalid token'}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            if user.role not in roles:
                return jsonify({'error': 'Access denied'}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    return role_required('Admin', 'HR')(fn)
