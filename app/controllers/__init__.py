"""
Controllers Package - Flask Blueprints
This package contains all route controllers for the HRSM System
"""

from app.controllers.auth_controller import auth_bp
from app.controllers.dashboard_controller import dashboard_bp
from app.controllers.leave_controller import leave_bp
from app.controllers.core_controller import core_bp

__all__ = ['auth_bp', 'dashboard_bp', 'leave_bp', 'core_bp']
