"""User CRUD API endpoints."""

from flask import Blueprint, request, g
from sqlalchemy.exc import IntegrityError
from database import db
from models.user import User
from auth.decorators import login_required, same_user_or_admin
from auth.password_utils import validate_username, validate_email, validate_password_strength
from utils.responses import (
    success_response, error_response, validation_error_response,
    not_found_response, conflict_response, forbidden_response
)

# Create blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@same_user_or_admin
def get_user(user_id):
    """Get user profile by ID.
    
    Args:
        user_id: User ID to retrieve
        
    Returns:
        200: User profile data
        401: Not authenticated
        403: Access denied
        404: User not found
    """
    try:
        user = User.find_by_id(user_id)
        if not user:
            return not_found_response("User not found")
        
        return success_response(
            data=user.to_dict(),
            message="User profile retrieved successfully"
        )
        
    except Exception as e:
        return error_response(f"Failed to retrieve user: {str(e)}")

@users_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
@same_user_or_admin
def update_user(user_id):
    """Update user profile.
    
    Args:
        user_id: User ID to update
        
    Expected JSON (all fields optional):
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    
    Returns:
        200: User updated successfully
        400: Validation error
        401: Not authenticated
        403: Access denied
        404: User not found
        409: Username or email conflict
    """
    try:
        # Get user to update
        user = User.find_by_id(user_id)
        if not user:
            return not_found_response("User not found")
        
        # Get JSON data
        data = request.get_json()
        if not data:
            return validation_error_response("Request body must be JSON")
        
        # Extract optional fields
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate username if provided
        if username is not None:
            username = username.strip()
            if username:  # Only validate if not empty
                is_valid, error_msg = validate_username(username)
                if not is_valid:
                    return validation_error_response(error_msg)
            else:
                username = None  # Treat empty string as None
        
        # Validate email if provided
        if email is not None:
            email = email.strip().lower()
            if email:  # Only validate if not empty
                is_valid, error_msg = validate_email(email)
                if not is_valid:
                    return validation_error_response(error_msg)
            else:
                email = None  # Treat empty string as None
        
        # Validate password if provided
        if password is not None:
            if password:  # Only validate if not empty
                is_valid, error_msg = validate_password_strength(password)
                if not is_valid:
                    return validation_error_response(error_msg)
            else:
                password = None  # Treat empty string as None
        
        # Check if at least one field is being updated
        if username is None and email is None and password is None:
            return validation_error_response("At least one field must be provided for update")
        
        # Update user profile
        try:
            updated = user.update_profile(
                username=username,
                email=email,
                password=password
            )
            
            if updated:
                db.session.commit()
                return success_response(
                    data=user.to_dict(),
                    message="User profile updated successfully"
                )
            else:
                return success_response(
                    data=user.to_dict(),
                    message="No changes were made"
                )
                
        except ValueError as e:
            db.session.rollback()
            return validation_error_response(str(e))
        except IntegrityError:
            db.session.rollback()
            return conflict_response("Username or email already exists")
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update user: {str(e)}")

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@same_user_or_admin
def delete_user(user_id):
    """Delete user account (soft delete by deactivation).
    
    Args:
        user_id: User ID to delete
        
    Returns:
        200: User deleted successfully
        401: Not authenticated
        403: Access denied
        404: User not found
    """
    try:
        user = User.find_by_id(user_id)
        if not user:
            return not_found_response("User not found")
        
        # Soft delete by deactivating the user
        user.deactivate()
        db.session.commit()
        
        # If user is deleting their own account, log them out
        if g.current_user.id == user_id:
            from auth.middleware import AuthMiddleware
            AuthMiddleware.logout_user()
        
        return success_response(
            data=None,
            message="User account deleted successfully"
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to delete user: {str(e)}")

@users_bp.route('/<int:user_id>/change-password', methods=['POST'])
@login_required
@same_user_or_admin
def change_password(user_id):
    """Change user password with current password verification.
    
    Args:
        user_id: User ID to change password for
        
    Expected JSON:
    {
        "current_password": "string",
        "new_password": "string"
    }
    
    Returns:
        200: Password changed successfully
        400: Validation error
        401: Not authenticated or invalid current password
        403: Access denied
        404: User not found
    """
    try:
        user = User.find_by_id(user_id)
        if not user:
            return not_found_response("User not found")
        
        # Get JSON data
        data = request.get_json()
        if not data:
            return validation_error_response("Request body must be JSON")
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Validate required fields
        if not current_password:
            return validation_error_response("Current password is required")
        if not new_password:
            return validation_error_response("New password is required")
        
        # Verify current password (only if user is changing their own password)
        if g.current_user.id == user_id:
            if not user.check_password(current_password):
                return validation_error_response("Current password is incorrect")
        
        # Validate new password strength
        is_valid, error_msg = validate_password_strength(new_password)
        if not is_valid:
            return validation_error_response(error_msg)
        
        # Check if new password is different from current
        if user.check_password(new_password):
            return validation_error_response("New password must be different from current password")
        
        # Update password
        try:
            user.set_password(new_password)
            db.session.commit()
            
            return success_response(
                data=None,
                message="Password changed successfully"
            )
            
        except ValueError as e:
            db.session.rollback()
            return validation_error_response(str(e))
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to change password: {str(e)}")

@users_bp.route('/profile', methods=['GET'])
@login_required
def get_my_profile():
    """Get current user's profile (convenience endpoint).
    
    Returns:
        200: User profile data
        401: Not authenticated
    """
    try:
        return success_response(
            data=g.current_user.to_dict(),
            message="Profile retrieved successfully"
        )
        
    except Exception as e:
        return error_response(f"Failed to retrieve profile: {str(e)}")

@users_bp.route('/profile', methods=['PUT'])
@login_required
def update_my_profile():
    """Update current user's profile (convenience endpoint).
    
    Expected JSON (all fields optional):
    {
        "username": "string",
        "email": "string"
    }
    
    Note: Use /change-password endpoint for password changes
    
    Returns:
        200: Profile updated successfully
        400: Validation error
        401: Not authenticated
        409: Username or email conflict
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return validation_error_response("Request body must be JSON")
        
        # Remove password from data if present (use change-password endpoint)
        if 'password' in data:
            return validation_error_response("Use /change-password endpoint to change password")
        
        # Forward to update_user with current user's ID
        return update_user(g.current_user.id)
        
    except Exception as e:
        return error_response(f"Failed to update profile: {str(e)}")