from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.employee_model import EmployeeModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        
        user = EmployeeModel.verify_login(email, password)
        
        if user:
            session['employee_id'] = user['employee_id']
            session['department'] = user['department']
            session['staff_name'] = user['staff_name']
            
            if user['department'] == 'HR':
                return redirect(url_for('dashboard.admin_dashboardUI'))
            else:
                return redirect(url_for('dashboard.dashboardUI'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))