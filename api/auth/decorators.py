"""Authentication decorators for route protection."""

from functools import wraps
from flask import session, request, jsonify, g
from models.user import User
from utils.responses import unauthorized_response, forbidden_response

def login_required(f):
    """Decorator to require user authentication.
    
    Checks for valid user session and loads user into g.current_user.
    Returns 401 if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in via session
        user_id = session.get('user_id')
        
        if not user_id:
            return unauthorized_response("Authentication required")
        
        # Load user from database
        user = User.find_by_id(user_id)
        if not user:
            # Clear invalid session
            session.pop('user_id', None)
            return unauthorized_response("Invalid session")
        
        # Store user in Flask's g object for access in route
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges.
    
    Must be used in combination with @login_required.
    Returns 403 if user is not admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is loaded (should be done by @login_required)
        if not hasattr(g, 'current_user') or not g.current_user:
            return unauthorized_response("Authentication required")
        
        # For now, we'll implement a simple admin check
        # In a real application, you might have an is_admin field or role system
        # For this implementation, we'll check if username is 'admin'
        if g.current_user.username != 'admin':
            return forbidden_response("Admin privileges required")
        
        return f(*args, **kwargs)
    
    return decorated_function

def optional_auth(f):
    """Decorator for optional authentication.
    
    Loads user if authenticated, but doesn't require it.
    Sets g.current_user to None if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        
        if user_id:
            user = User.find_by_id(user_id)
            g.current_user = user if user else None
        else:
            g.current_user = None
        
        return f(*args, **kwargs)
    
    return decorated_function

def same_user_or_admin(f):
    """Decorator to allow access to own resources or admin.
    
    Checks if the authenticated user is accessing their own resource
    or if they have admin privileges.
    Expects 'user_id' parameter in the route.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is loaded (should be done by @login_required)
        if not hasattr(g, 'current_user') or not g.current_user:
            return unauthorized_response("Authentication required")
        
        # Get the user_id from route parameters
        target_user_id = kwargs.get('user_id') or kwargs.get('id')
        
        if not target_user_id:
            return forbidden_response("Invalid request")
        
        # Convert to int if it's a string
        try:
            target_user_id = int(target_user_id)
        except (ValueError, TypeError):
            return forbidden_response("Invalid user ID")
        
        # Allow if user is accessing their own resource
        if g.current_user.id == target_user_id:
            return f(*args, **kwargs)
        
        # Allow if user is admin
        if g.current_user.username == 'admin':
            return f(*args, **kwargs)
        
        return forbidden_response("Access denied")
    
    return decorated_function