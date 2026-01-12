from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Employee, Payroll
from utils.decorators import admin_required
from utils.helpers import create_notification
from datetime import datetime

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/my-payroll', methods=['GET'])
@jwt_required()
def get_my_payroll():
    """Get logged-in user's payroll history"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        employee = Employee.query.filter_by(user_id=user_id).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        year = request.args.get('year', datetime.now().year, type=int)
        
        payrolls = Payroll.query.filter_by(
            employee_id=employee.id,
            year=year
        ).order_by(Payroll.month.desc()).all()
        
        return jsonify({
            'payrolls': [p.to_dict() for p in payrolls]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payroll_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_payslip(id):
    """Get specific payslip"""
    try:
        # ✅ FIX: Convert string to int
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        payroll = Payroll.query.get_or_404(id)
        
        if user.role == 'Employee':
            employee = Employee.query.filter_by(user_id=user_id).first()
            if payroll.employee_id != employee.id:
                return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'payroll': payroll.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payroll_bp.route('/all', methods=['GET'])
@jwt_required()
@admin_required
def get_all_payroll():
    """Get all payroll records - Admin only"""
    try:
        month = request.args.get('month', type=int)
        year = request.args.get('year', datetime.now().year, type=int)
        department = request.args.get('department')
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Payroll.query.filter_by(year=year)
        
        if month:
            query = query.filter_by(month=month)
        
        if department:
            query = query.join(Employee).filter(Employee.department == department)
        
        if status:
            query = query.filter_by(payment_status=status)
        
        payrolls = query.paginate(page=page, per_page=per_page)
        
        all_payrolls = query.all()
        total_gross = sum(float(p.gross_salary or 0) for p in all_payrolls)
        total_net = sum(float(p.net_salary or 0) for p in all_payrolls)
        
        return jsonify({
            'payrolls': [p.to_dict() for p in payrolls.items],
            'total': payrolls.total,
            'pages': payrolls.pages,
            'current_page': page,
            'summary': {
                'total_gross_salary': total_gross,
                'total_net_salary': total_net,
                'total_employees': len(all_payrolls)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payroll_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_payroll():
    """Create or update payroll - Admin only"""
    try:
        data = request.get_json()
        
        required = ['employee_id', 'month', 'year', 'basic_salary']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        existing = Payroll.query.filter_by(
            employee_id=data['employee_id'],
            month=data['month'],
            year=data['year']
        ).first()
        
        if existing:
            payroll = existing
        else:
            payroll = Payroll(
                employee_id=data['employee_id'],
                month=data['month'],
                year=data['year']
            )
        
        payroll.basic_salary = data['basic_salary']
        payroll.hra = data.get('hra', 0)
        payroll.da = data.get('da', 0)
        payroll.ta = data.get('ta', 0)
        payroll.other_allowances = data.get('other_allowances', 0)
        payroll.pf_deduction = data.get('pf_deduction', 0)
        payroll.tax_deduction = data.get('tax_deduction', 0)
        payroll.other_deductions = data.get('other_deductions', 0)
        
        payroll.calculate_salary()
        
        if not existing:
            db.session.add(payroll)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payroll saved successfully',
            'payroll': payroll.to_dict()
        }), 201 if not existing else 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payroll_bp.route('/<int:id>/process', methods=['PUT'])
@jwt_required()
@admin_required
def process_payroll(id):
    """Process payroll payment - Admin only"""
    try:
        payroll = Payroll.query.get_or_404(id)
        data = request.get_json()
        
        payroll.payment_status = data.get('status', 'Processed')
        
        if data.get('payment_date'):
            payroll.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
        
        month_name = datetime(payroll.year, payroll.month, 1).strftime('%B')
        create_notification(
            employee_id=payroll.employee_id,
            title='Salary Processed',
            message=f'Your salary for {month_name} {payroll.year} has been processed. Net amount: Rs.{payroll.net_salary}',
            notification_type='Payroll',
            reference_id=payroll.id,
            reference_type='payroll'
        )
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payroll processed successfully',
            'payroll': payroll.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payroll_bp.route('/generate-bulk', methods=['POST'])
@jwt_required()
@admin_required
def generate_bulk_payroll():
    """Generate payroll for all employees - Admin only"""
    try:
        data = request.get_json()
        month = data.get('month', datetime.now().month)
        year = data.get('year', datetime.now().year)
        
        employees = Employee.query.all()
        created_count = 0
        
        for emp in employees:
            existing = Payroll.query.filter_by(
                employee_id=emp.id,
                month=month,
                year=year
            ).first()
            
            if not existing:
                prev_payroll = Payroll.query.filter_by(
                    employee_id=emp.id
                ).order_by(Payroll.year.desc(), Payroll.month.desc()).first()
                
                if prev_payroll:
                    payroll = Payroll(
                        employee_id=emp.id,
                        month=month,
                        year=year,
                        basic_salary=prev_payroll.basic_salary,
                        hra=prev_payroll.hra,
                        da=prev_payroll.da,
                        ta=prev_payroll.ta,
                        other_allowances=prev_payroll.other_allowances,
                        pf_deduction=prev_payroll.pf_deduction,
                        tax_deduction=prev_payroll.tax_deduction,
                        other_deductions=prev_payroll.other_deductions
                    )
                    payroll.calculate_salary()
                    db.session.add(payroll)
                    created_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'Generated payroll for {created_count} employees',
            'month': month,
            'year': year
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500