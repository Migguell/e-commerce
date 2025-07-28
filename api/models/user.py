from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from database import db
import bcrypt
import re

class User(db.Model):
    """User model for authentication and user management."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, username, email, password, is_active=True):
        """Initialize a new user with hashed password."""
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_active = is_active
    
    def set_password(self, password):
        """Hash and set the user's password."""
        if not self.validate_password(password):
            raise ValueError("Password does not meet security requirements")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches the stored hash."""
        if not password or not self.password_hash:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    @staticmethod
    def validate_username(username):
        """Validate username format and length."""
        if not username:
            return False, "Username is required"
        
        if len(username) < 3 or len(username) > 50:
            return False, "Username must be between 3 and 50 characters"
        
        # Allow alphanumeric characters and underscores only
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, None
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        if not email:
            return False, "Email is required"
        
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 255:
            return False, "Email must be less than 255 characters"
        
        return True, None
    
    @staticmethod
    def validate_password(password):
        """Validate password complexity requirements."""
        if not password:
            return False, "Password is required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        return True, None
    
    @classmethod
    def find_by_username(cls, username):
        """Find user by username."""
        return cls.query.filter_by(username=username, is_active=True).first()
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email."""
        return cls.query.filter_by(email=email, is_active=True).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        return cls.query.filter_by(id=user_id, is_active=True).first()
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary for JSON serialization."""
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Never include password hash in normal serialization
        if include_sensitive:
            # Even in sensitive mode, we don't include the actual password
            user_dict['has_password'] = bool(self.password_hash)
        
        return user_dict
    
    def update_profile(self, username=None, email=None, password=None):
        """Update user profile with validation."""
        updated = False
        
        if username is not None and username != self.username:
            is_valid, error = self.validate_username(username)
            if not is_valid:
                raise ValueError(f"Invalid username: {error}")
            
            # Check if username is already taken
            existing_user = User.find_by_username(username)
            if existing_user and existing_user.id != self.id:
                raise ValueError("Username is already taken")
            
            self.username = username
            updated = True
        
        if email is not None and email != self.email:
            is_valid, error = self.validate_email(email)
            if not is_valid:
                raise ValueError(f"Invalid email: {error}")
            
            # Check if email is already taken
            existing_user = User.find_by_email(email)
            if existing_user and existing_user.id != self.id:
                raise ValueError("Email is already taken")
            
            self.email = email
            updated = True
        
        if password is not None:
            self.set_password(password)
            updated = True
        
        if updated:
            self.updated_at = datetime.utcnow()
        
        return updated
    
    def deactivate(self):
        """Deactivate user account instead of hard delete."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<User {self.username} ({self.email})>'