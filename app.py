import os
from flask import Flask
from app.db import get_all_entries

app = Flask(__name__)

@app.route('/')
def index():
    users = get_all_entries('user')

    html = '<h1>User</h1><ul>'
    for user in users:
        html += f'<li>{user["user_type"]} | {user["username"]}</li>'
    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run(debug=True)