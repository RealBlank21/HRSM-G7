from app.db import supabase
from datetime import datetime

class LeaveModel:
    @staticmethod
    def get_employee_leaves(employee_id: str):
        try:
            response = supabase.table('leave').select('*').eq('employee_id', employee_id).order('start_date', desc=True).execute()
            return response.data
        except Exception as e:
            print(e)
            return []
        
    @staticmethod
    def get_all_leaves():
        try:
            leaves_response = supabase.table('leave').select('*').order('start_date', desc=True).execute()
            leaves = leaves_response.data
            
            employees_response = supabase.table('employee').select('employee_id, staff_name').execute()
            employees = employees_response.data
            
            emp_map = {emp['employee_id']: emp['staff_name'] for emp in employees}
            
            for lv in leaves:
                lv['employee_name'] = emp_map.get(lv.get('employee_id'), 'Unknown')
                
            return leaves
        except Exception as e:
            print(e)
            return []
            
    @staticmethod
    def check_leave_balance(leaves):
        total_allowance = 30 
        total_used = 0
        
        for lv in leaves:
            if lv['status'] in ['Approved', 'Pending']:
                start = datetime.strptime(lv['start_date'], '%Y-%m-%d')
                end = datetime.strptime(lv['end_date'], '%Y-%m-%d')
                days_taken = (end - start).days + 1
                total_used += days_taken

        return total_allowance - total_used

    @staticmethod
    def save_leave_detail(data: dict):
        try:
            response = supabase.table('leave').insert(data).execute()
            return response.data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete_leave(leave_id: str):
        try:
            response = supabase.table('leave').delete().eq('leave_id', leave_id).execute()
            return response.data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_leave_detail(leave_id: str, data: dict):
        try:
            response = supabase.table('leave').update(data).eq('leave_id', leave_id).execute()
            return response.data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def review_accept_leave(leave_id: str):
        return LeaveModel.update_leave_detail(leave_id, {'status': 'Approved'})

    @staticmethod
    def review_reject_leave(leave_id: str, reason: str):
        return LeaveModel.update_leave_detail(leave_id, {'status': 'Rejected', 'rejection_reason': reason})