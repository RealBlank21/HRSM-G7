from app.db import supabase

class EmployeeModel:
    @staticmethod
    def verify_login(email: str, password: str):
        try:    
            response = supabase.table('employee').select('*').eq('email', email).eq('password', password).execute()
            if len(response.data) > 0:
                return response.data[0]
            return None
        except Exception:
            return None