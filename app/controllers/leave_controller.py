import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.leave_model import Leave
from datetime import datetime

leave_bp = Blueprint('leave', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@leave_bp.route('/leave', methods=['GET', 'POST'])
def leaveUI():
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    employee_id = session['employee_id']
    leaves = Leave.get_employee_leaves(employee_id)
    
    pending_leaves = [lv for lv in leaves if lv['status'] == 'Pending']
    other_leaves = [lv for lv in leaves if lv['status'] != 'Pending']
    leaves = pending_leaves + other_leaves

    leave_obj = Leave()
    leave_obj.employee_id = employee_id
    total_remaining_balance = leave_obj.checkLeaveBalance()

    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        start = datetime.strptime(start_date_str, '%Y-%m-%d')
        end = datetime.strptime(end_date_str, '%Y-%m-%d')
        days_requested = (end - start).days + 1
        
        if days_requested > total_remaining_balance:
            flash('Insufficient Balance to request this leave.', 'error')
            return redirect(url_for('leave.leaveUI'))

        attachment_doc_url = None
        attachment = request.files.get('attachment')
        if attachment and attachment.filename:
            filename = secure_filename(attachment.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_filename = f"{employee_id}_{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            attachment.save(filepath)
            attachment_doc_url = f"/static/uploads/{unique_filename}"

        leave = Leave()
        leave.leaveID = None
        leave.employee_id = employee_id
        leave.leaveType = request.form.get('leaveType')
        leave.description = request.form.get('description')
        leave.startDate = start_date_str
        leave.endDate = end_date_str
        leave.status = 'Pending'
        leave.submittedDate = datetime.now().strftime('%Y-%m-%d')
        leave.attachmentDocURL = attachment_doc_url
        
        leave.saveLeaveDetail()
        
        flash('Your leave has been submitted successfully.', 'success')
        return redirect(url_for('leave.leaveUI'))
    
    return render_template('employee-leave.html', 
                         leaves=leaves, 
                         total_remaining_balance=total_remaining_balance)

@leave_bp.route('/leave/update/<leave_id>', methods=['POST'])
def update_leave(leave_id):
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    leaves = Leave.get_employee_leaves(session['employee_id'])
    leave_data = None
    for lv in leaves:
        if lv['leave_id'] == leave_id:
            leave_data = lv
            break
    
    if not leave_data:
        flash('Leave not found.', 'error')
        return redirect(url_for('leave.leaveUI'))
    
    if leave_data['employee_id'] != session['employee_id']:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('leave.leaveUI'))
    
    if leave_data['status'] != 'Pending':
        flash('Cannot update non-pending leave.', 'error')
        return redirect(url_for('leave.leaveUI'))
    
    leave = Leave()
    leave.leaveID = leave_id
    leave.employee_id = session['employee_id']
    leave.leaveType = request.form.get('leaveType')
    leave.description = request.form.get('description')
    leave.startDate = request.form.get('start_date')
    leave.endDate = request.form.get('end_date')
    leave.status = 'Pending'
    leave.submittedDate = leave_data['submitted_date']
    leave.attachmentDocURL = leave_data.get('attachment_doc_url')
    
    attachment = request.files.get('attachment')
    if attachment and attachment.filename:
        filename = secure_filename(attachment.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{session['employee_id']}_{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        attachment.save(filepath)
        leave.attachmentDocURL = f"/static/uploads/{unique_filename}"

    leave.updateLeaveDetail()
    
    flash('Your leave has been updated successfully.', 'success')
    return redirect(url_for('leave.leaveUI'))

@leave_bp.route('/leave/delete/<leave_id>', methods=['POST'])
def delete_leave(leave_id):
    if 'employee_id' not in session:
        return redirect(url_for('auth.index'))
    
    leaves = Leave.get_employee_leaves(session['employee_id'])
    leave_data = None
    for lv in leaves:
        if lv['leave_id'] == leave_id:
            leave_data = lv
            break
    
    if not leave_data:
        flash('Leave not found.', 'error')
        return redirect(url_for('leave.leaveUI'))
    
    if leave_data['status'] != 'Pending':
        flash('Cannot delete non-pending leave.', 'error')
        return redirect(url_for('leave.leaveUI'))
    
    leave = Leave()
    leave.leaveID = leave_id
    leave.deleteLeave()
    
    flash('Your leave has been deleted successfully.', 'success')
    return redirect(url_for('leave.leaveUI'))

@leave_bp.route('/admin/leave')
def admin_leaveUI():
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    leaves = Leave.get_all_leaves()
    
    pending_leaves = [lv for lv in leaves if lv['status'] == 'Pending']
    other_leaves = [lv for lv in leaves if lv['status'] != 'Pending']
    leaves = pending_leaves + other_leaves

    return render_template('admin-leave.html', leaves=leaves)

@leave_bp.route('/admin/leave/approve/<leave_id>', methods=['POST'])
def admin_approve_leave(leave_id):
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    leave = Leave()
    leave.leaveID = leave_id
    leave.reviewAcceptLeave()
    
    flash('Employee leave has been approved successfully.', 'success')
    return redirect(url_for('leave.admin_leaveUI'))

@leave_bp.route('/admin/leave/reject/<leave_id>', methods=['POST'])
def admin_reject_leave(leave_id):
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('auth.index'))
    
    reason = request.form.get('rejectionReason')
    
    if not reason or not reason.strip():
        flash('Rejection reason is required.', 'error')
        return redirect(url_for('leave.admin_leaveUI'))
    
    leave = Leave()
    leave.leaveID = leave_id
    leave.reviewRejectLeave(reason.strip())
    
    flash('Employee leave has been rejected successfully.', 'success')
    return redirect(url_for('leave.admin_leaveUI'))
