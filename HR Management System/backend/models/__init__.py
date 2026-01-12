from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .employee import Employee
from .attendance import Attendance
from .leave import LeaveRequest
from .payroll import Payroll
from .notification import Notification