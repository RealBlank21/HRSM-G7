from app.db import supabase
from flask import session

class Employee:
    def __init__(self):
        self.employee_id = None
        self.email = None
        self.password = None
        self.staff_name = None
        self.department = None
    
    def verify_login(self, email, password):
        try:
            response = supabase.table('employee').select('*').eq('email', email).eq('password', password).execute()
            if len(response.data) > 0:
                self.employee_id = response.data[0]['employee_id']
                self.email = response.data[0]['email']
                self.staff_name = response.data[0]['staff_name']
                self.department = response.data[0]['department']
                return response.data[0]
            return None
        except Exception as e:
            print(e)
            return None
    
    def set_session(self):
        session['employee_id'] = self.employee_id
        session['department'] = self.department
        session['staff_name'] = self.staff_name
    
    def clear_session(self):
        session.clear()
    
    def is_hr(self):
        return self.department == 'HR'
