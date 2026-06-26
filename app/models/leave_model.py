from app.db import supabase
from datetime import datetime

class Leave:
    def __init__(self):
        self.leaveID = None
        self.leaveType = None
        self.description = None
        self.startDate = None
        self.endDate = None
        self.status = 'Pending'
        self.submittedDate = None
        self.attachmentDocURL = None
        self.rejectionReason = None
        self.employee_id = None
    
    def checkLeaveBalance(self):
        try:
            response = supabase.table('leave').select('*').eq('employee_id', self.employee_id).execute()
            leaves = response.data if response.data else []
            
            total_allowance = 30
            total_used = 0
            
            for lv in leaves:
                if lv['status'] in ['Approved', 'Pending']:
                    start = datetime.strptime(lv['start_date'], '%Y-%m-%d')
                    end = datetime.strptime(lv['end_date'], '%Y-%m-%d')
                    days_taken = (end - start).days + 1
                    total_used += days_taken
            
            return total_allowance - total_used
        except Exception as e:
            print(e)
            return 0
    
    def saveLeaveDetail(self):
        try:
            data = {
                'leave_id': self.leaveID,
                'employee_id': self.employee_id,
                'leave_type': self.leaveType,
                'description': self.description,
                'start_date': self.startDate,
                'end_date': self.endDate,
                'status': self.status,
                'submitted_date': self.submittedDate,
                'attachment_doc_url': self.attachmentDocURL,
                'rejection_reason': self.rejectionReason
            }
            
            if self.leaveID:
                response = supabase.table('leave').update(data).eq('leave_id', self.leaveID).execute()
            else:
                response = supabase.table('leave').insert(data).execute()
                if len(response.data) > 0:
                    self.leaveID = response.data[0]['leave_id']
            
            return response.data
        except Exception as e:
            print(e)
            return None

    def deleteLeave(self):
        try:
            response = supabase.table('leave').delete().eq('leave_id', self.leaveID).execute()
            return response.data
        except Exception as e:
            print(e)
            return None
    
    def updateLeaveDetail(self):
        return self.saveLeaveDetail()
    
    def reviewAcceptLeave(self):
        try:
            self.status = 'Approved'
            data = {'status': 'Approved'}
            response = supabase.table('leave').update(data).eq('leave_id', self.leaveID).execute()
            return response.data
        except Exception as e:
            print(e)
            return None
    
    def reviewRejectLeave(self, reason):
        try:
            self.status = 'Rejected'
            self.rejectionReason = reason
            data = {'status': 'Rejected', 'rejection_reason': reason}
            response = supabase.table('leave').update(data).eq('leave_id', self.leaveID).execute()
            return response.data
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def get_all_leaves():
        try:
            leaves_response = supabase.table('leave').select('*').order('start_date', desc=True).execute()
            leaves = leaves_response.data if leaves_response.data else []
            
            employees_response = supabase.table('employee').select('employee_id, staff_name').execute()
            employees = employees_response.data if employees_response.data else []
            
            emp_map = {emp['employee_id']: emp['staff_name'] for emp in employees}
            
            for lv in leaves:
                lv['employee_name'] = emp_map.get(lv.get('employee_id'), 'Unknown')
                
            return leaves
        except Exception as e:
            print(e)
            return []
    
    @staticmethod
    def get_employee_leaves(employee_id):
        try:
            response = supabase.table('leave').select('*').eq('employee_id', employee_id).order('start_date', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(e)
            return []
