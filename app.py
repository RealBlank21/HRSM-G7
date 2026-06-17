import os
from flask import Flask, render_template
from app.db import get_all_entries

app = Flask(__name__)

@app.route('/')
def index():
    # users = get_all_entries('user')

    # html = '<h1>User</h1><ul>'
    # for user in users:
    #     html += f'<li>{user["user_type"]} | {user["username"]}</li>'
    # html += '</ul>'

    # return html

    return render_template('login.html')

@app.route('/dashboard')
def dashboardUI():
    return render_template('employee-dashboard.html')

@app.route('/leave')
def leaveUI():
    return render_template('employee-leave.html')

@app.route('/claim')
def claimUI():
    return render_template('employee-claim.html')

@app.route('/payroll')
def payrollUI():
    return render_template('employee-payroll.html')

@app.route('/feedback')
def feedbackUI():
    return render_template('employee-feedback.html')

@app.route('/logout')
def logout():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)