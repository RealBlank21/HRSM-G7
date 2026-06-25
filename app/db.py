import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

def get_all_entries(table_name: str):
    try:
        response = supabase.table(table_name).select("*").execute()
        return response.data
    except Exception as e:
        return []

def verify_login(email: str, password: str):
    try:    
        response = supabase.table('employee').select('*').eq('email', email).eq('password', password).execute()
        if len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        return None
    
def get_employee_leaves(employee_id: str):
    try:
        # Fetch leaves and order them by newest first
        response = supabase.table('leave').select('*').eq('employee_id', employee_id).order('start_date', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Database Error [get_employee_leaves]: {e}")
        return []