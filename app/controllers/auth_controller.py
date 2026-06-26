from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.employee_model import Employee

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        
        employee = Employee()
        user = employee.verify_login(email, password)
        
        if user:
            employee.set_session()
            
            if employee.is_hr():
                return redirect(url_for('dashboard.admin_dashboardUI'))
            else:
                return redirect(url_for('dashboard.dashboardUI'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    employee = Employee()
    employee.clear_session()
    return redirect(url_for('auth.index'))
