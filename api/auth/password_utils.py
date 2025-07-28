"""Password hashing and verification utilities using bcrypt."""

import bcrypt
import re
from typing import Tuple

def hash_password(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password as string
        
    Raises:
        ValueError: If password doesn't meet requirements
    """
    if not validate_password_strength(password)[0]:
        raise ValueError("Password does not meet security requirements")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)  # Higher rounds for better security
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Stored password hash
        
    Returns:
        True if password matches hash, False otherwise
    """
    if not password or not hashed_password:
        return False
    
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except (ValueError, TypeError):
        return False

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validate password meets security requirements.
    
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters long"
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, ""

def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username format and length.
    
    Requirements:
    - 3-50 characters long
    - Alphanumeric characters and underscores only
    - Cannot start with underscore
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters"
    
    # Cannot start with underscore
    if username.startswith('_'):
        return False, "Username cannot start with underscore"
    
    # Allow alphanumeric characters and underscores only
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format.
    
    Args:
        email: Email to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    if len(email) > 255:
        return False, "Email must be less than 255 characters"
    
    # Basic email validation regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    return True, ""