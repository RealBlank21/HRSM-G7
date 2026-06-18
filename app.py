import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.db import get_all_entries, verify_login
from datetime import datetime

from app.db import get_all_entries, get_employee_leaves

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hrms-assignment-secret-key-123")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        
        user = verify_login(email, password)
        
        if user:
            session['employee_id'] = user['employee_id']
            session['department'] = user['department']
            session['staff_name'] = user['staff_name']
            
            if user['department'] == 'HR':
                return redirect(url_for('admin_dashboardUI'))
            else:
                return redirect(url_for('dashboardUI'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboardUI():
    if 'employee_id' not in session:
        return redirect(url_for('index'))
    return render_template('employee-dashboard.html')

@app.route('/admin/dashboard')
def admin_dashboardUI():
    if 'employee_id' not in session or session.get('department') != 'HR':
        return redirect(url_for('index'))
    return render_template('admin-dashboard.html')

@app.route('/leave')
def leaveUI():
    if 'employee_id' not in session:
        return redirect(url_for('index'))
    
    employee_id = session['employee_id']
    leaves = get_employee_leaves(employee_id)
    
    total_allowance = 30 
    total_used = 0
    
    for lv in leaves:
        if lv['status'] in ['Approved', 'Pending']:
            start = datetime.strptime(lv['start_date'], '%Y-%m-%d')
            end = datetime.strptime(lv['end_date'], '%Y-%m-%d')
            days_taken = (end - start).days + 1
            total_used += days_taken

    total_remaining_balance = total_allowance - total_used
    
    return render_template('employee-leave.html', leaves=leaves, total_remaining_balance=total_remaining_balance)

@app.route('/claim')
def claimUI():
    if 'employee_id' not in session:
        return redirect(url_for('index'))
    return render_template('employee-claim.html')

@app.route('/payroll')
def payrollUI():
    if 'employee_id' not in session:
        return redirect(url_for('index'))
    return render_template('employee-payroll.html')

@app.route('/feedback')
def feedbackUI():
    if 'employee_id' not in session:
        return redirect(url_for('index'))
    return render_template('employee-feedback.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)