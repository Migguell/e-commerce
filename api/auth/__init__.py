"""Authentication package for the e-commerce backend API.

This package contains authentication-related functionality:
- middleware: Authentication middleware for request processing
- decorators: Authentication decorators for route protection
- password_utils: Password hashing and verification utilities
"""

from .middleware import AuthMiddleware
from .decorators import login_required, admin_required
from .password_utils import hash_password, verify_password

__all__ = [
    'AuthMiddleware',
    'login_required',
    'admin_required', 
    'hash_password',
    'verify_password'
]