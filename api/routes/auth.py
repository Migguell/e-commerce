"""Authentication API endpoints."""

from flask import Blueprint, request, session
from sqlalchemy.exc import IntegrityError
from database import db
from models.user import User
from auth.middleware import AuthMiddleware
from auth.password_utils import validate_username, validate_email, validate_password_strength
from utils.responses import (
    success_response, error_response, validation_error_response,
    created_response, unauthorized_response, conflict_response
)
from utils.exceptions import ValidationError, ConflictError

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account.
    
    Expected JSON:
    {
        "username": "string",
        "email": "string", 
        "password": "string"
    }
    
    Returns:
        201: User created successfully
        400: Validation error
        409: Username or email already exists
        500: Server error
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return validation_error_response("Request body must be JSON")
        
        # Extract required fields
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not username:
            return validation_error_response("Username is required")
        if not email:
            return validation_error_response("Email is required")
        if not password:
            return validation_error_response("Password is required")
        
        # Validate username format
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return validation_error_response(error_msg)
        
        # Validate email format
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return validation_error_response(error_msg)
        
        # Validate password strength
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            return validation_error_response(error_msg)
        
        # Check if username already exists
        existing_user = User.find_by_username(username)
        if existing_user:
            return conflict_response("Username is already taken")
        
        # Check if email already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return conflict_response("Email is already registered")
        
        # Create new user
        try:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            
            # Log in the user automatically
            AuthMiddleware.login_user(user)
            
            return created_response(
                data=user.to_dict(),
                message="User registered successfully"
            )
            
        except IntegrityError:
            db.session.rollback()
            return conflict_response("Username or email already exists")
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Registration failed: {str(e)}")

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and create session.
    
    Expected JSON:
    {
        "username": "string",  # or "email"
        "password": "string"
    }
    
    Returns:
        200: Login successful
        400: Validation error
        401: Invalid credentials
        500: Server error
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return validation_error_response("Request body must be JSON")
        
        # Extract credentials
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Must provide either username or email
        if not username and not email:
            return validation_error_response("Username or email is required")
        
        if not password:
            return validation_error_response("Password is required")
        
        # Find user by username or email
        user = None
        if username:
            user = User.find_by_username(username)
        elif email:
            user = User.find_by_email(email)
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            return unauthorized_response("Invalid username/email or password")
        
        # Log in the user
        AuthMiddleware.login_user(user)
        
        return success_response(
            data=user.to_dict(),
            message="Login successful"
        )
        
    except Exception as e:
        return error_response(f"Login failed: {str(e)}")

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Log out the current user.
    
    Returns:
        200: Logout successful
    """
    try:
        AuthMiddleware.logout_user()
        return success_response(
            data=None,
            message="Logout successful"
        )
        
    except Exception as e:
        return error_response(f"Logout failed: {str(e)}")

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current authenticated user information.
    
    Returns:
        200: User information
        401: Not authenticated
    """
    try:
        user = AuthMiddleware.get_current_user()
        if not user:
            return unauthorized_response("Not authenticated")
        
        return success_response(
            data=user.to_dict(),
            message="User information retrieved"
        )
        
    except Exception as e:
        return error_response(f"Failed to get user information: {str(e)}")

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated.
    
    Returns:
        200: Authentication status
    """
    try:
        is_authenticated = AuthMiddleware.is_authenticated()
        user = AuthMiddleware.get_current_user()
        
        return success_response(
            data={
                'authenticated': is_authenticated,
                'user': user.to_dict() if user else None
            },
            message="Authentication status checked"
        )
        
    except Exception as e:
        return error_response(f"Failed to check authentication: {str(e)}")