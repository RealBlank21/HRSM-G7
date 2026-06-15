import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

@app.route('/')
def index():
    response = supabase.table('user').select("*").execute()
    users = response.data

    html = '<h1>User</h1><ul>'
    for user in users:
        html += f'<li>{user["user_type"]} |{user["username"]}</li>'
    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run(debug=True)