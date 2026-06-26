from flask import Blueprint, render_template, redirect, url_for, session

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboardUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('employee-dashboard.html')

@dashboard_bp.route('/admin/dashboard')
def admin_dashboardUI():
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    return render_template('admin-dashboard.html')