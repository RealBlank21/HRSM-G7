from flask import Blueprint, render_template, redirect, url_for, session
from app.models.leave_model import Leave
from app.models.employee_model import Employee

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboardUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    employee = Employee()
    # 加载员工信息
    employee.verify_login(session['employee_id'], '')  # 简化，直接设属性
    employee.employee_id = session['employee_id']
    employee.staff_name = session['staff_name']
    
    leave_stats = {'total': 0, 'pending': 0, 'approved': 0, 'rejected': 0}  # 简化
    recent_leaves = Leave.get_employee_leaves(session['employee_id'])[:5]
    
    return render_template('employee-dashboard.html', 
                         employee=employee,
                         leave_stats=leave_stats,
                         recent_leaves=recent_leaves)

@dashboard_bp.route('/admin/dashboard')
def admin_dashboardUI():
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    admin = Employee()
    admin.employee_id = session['employee_id']
    admin.staff_name = session['staff_name']
    
    leaves = Leave.get_all_leaves()
    pending_leaves = [lv for lv in leaves if lv['status'] == 'Pending']
    leave_stats = {'total': len(leaves), 'pending': len(pending_leaves), 'approved': 0, 'rejected': 0}
    
    return render_template('admin-dashboard.html',
                         admin=admin,
                         leave_stats=leave_stats,
                         pending_leaves=pending_leaves,
                         total_employees=10)  # 简化
