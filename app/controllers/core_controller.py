from flask import Blueprint, render_template, redirect, url_for, session

core_bp = Blueprint('core', __name__)

@core_bp.route('/claim')
def claimUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('employee-claim.html')

@core_bp.route('/payroll')
def payrollUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('employee-payroll.html')

@core_bp.route('/feedback')
def feedbackUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('employee-feedback.html')