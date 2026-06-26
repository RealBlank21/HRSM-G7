from app.db import supabase

class BaseModel:
    @staticmethod
    def get_all_entries(table_name: str):
        try:
            response = supabase.table(table_name).select("*").execute()
            return response.data
        except Exception:
            return []