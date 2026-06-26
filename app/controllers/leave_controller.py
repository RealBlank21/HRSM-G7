from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.leave_model import LeaveModel
from datetime import datetime

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/leave', methods=['GET', 'POST'])
def leaveUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    employee_id = session['employee_id']
    leaves = LeaveModel.get_employee_leaves(employee_id)
    total_remaining_balance = LeaveModel.calculate_leave_balance(leaves)

    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        start = datetime.strptime(start_date_str, '%Y-%m-%d')
        end = datetime.strptime(end_date_str, '%Y-%m-%d')
        days_requested = (end - start).days + 1
        
        if days_requested > total_remaining_balance:
            flash('E-1: Insufficient Balance to request this leave.', 'error')
            return redirect(url_for('leave.leaveUI'))

        data = {
            'employee_id': employee_id,
            'leave_type': request.form.get('leaveType'),
            'description': request.form.get('description'),
            'start_date': start_date_str,
            'end_date': end_date_str,
            'status': 'Pending',
            'submitted_date': datetime.now().strftime('%Y-%m-%d')
        }

        LeaveModel.save_leave_detail(data)

        return redirect(url_for('leave.leaveUI'))
    
    return render_template('employee-leave.html', leaves=leaves, total_remaining_balance=total_remaining_balance)

@leave_bp.route('/leave/update/<leave_id>', methods=['POST'])
def update_leave(leave_id):
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    data = {
        'leave_type': request.form.get('leaveType'),
        'description': request.form.get('description'),
        'start_date': request.form.get('start_date'),
        'end_date': request.form.get('end_date')
    }
    LeaveModel.update_leave_detail(leave_id, data)
    return redirect(url_for('leave.leaveUI'))

@leave_bp.route('/leave/delete/<leave_id>', methods=['POST'])
def delete_leave(leave_id):
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    LeaveModel.delete_leave(leave_id)
    return redirect(url_for('leave.leaveUI'))

@leave_bp.route('/admin/leave')
def admin_leaveUI():
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    leaves = LeaveModel.get_all_leaves()
    return render_template('admin-leave.html', leaves=leaves)

@leave_bp.route('/admin/leave/approve/<leave_id>', methods=['POST'])
def admin_approve_leave(leave_id):
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    LeaveModel.review_accept_leave(leave_id)
    return redirect(url_for('leave.admin_leaveUI'))

@leave_bp.route('/admin/leave/reject/<leave_id>', methods=['POST'])
def admin_reject_leave(leave_id):
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    reason = request.form.get('rejectionReason', 'Not specified')
    LeaveModel.review_reject_leave(leave_id, reason)
    return redirect(url_for('leave.admin_leaveUI'))