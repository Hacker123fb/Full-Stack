from .auth import auth_bp
from .employee import employee_bp
from .attendance import attendance_bp
from .leave import leave_bp
from .payroll import payroll_bp
from .notification import notification_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(leave_bp, url_prefix='/api/leaves')
    app.register_blueprint(payroll_bp, url_prefix='/api/payroll')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')