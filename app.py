import os
from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.dashboard_controller import dashboard_bp
from app.controllers.leave_controller import leave_bp
from app.controllers.core_controller import core_bp

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hrms-assignment-secret-key-123")

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(leave_bp)
app.register_blueprint(core_bp)

if __name__ == '__main__':
    app.run(debug=True)