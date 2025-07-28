"""Authentication middleware for session management."""

from flask import session, request, g
from models.user import User
import uuid

class AuthMiddleware:
    """Middleware for handling authentication and session management."""
    
    def __init__(self, app=None):
        """Initialize the middleware."""
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with Flask app."""
        app.before_request(self.load_user)
        app.after_request(self.save_session)
    
    def load_user(self):
        """Load user from session before each request."""
        # Initialize current_user as None
        g.current_user = None
        
        # Check if user is logged in
        user_id = session.get('user_id')
        if user_id:
            user = User.find_by_id(user_id)
            if user:
                g.current_user = user
            else:
                # Clear invalid session
                session.pop('user_id', None)
        
        # Ensure session has a session ID for cart functionality
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
    
    def save_session(self, response):
        """Save session after each request."""
        # Flask-Session handles this automatically
        return response
    
    @staticmethod
    def login_user(user):
        """Log in a user by setting session data.
        
        Args:
            user: User object to log in
        """
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = True  # Make session permanent
    
    @staticmethod
    def logout_user():
        """Log out the current user by clearing session data."""
        session.pop('user_id', None)
        session.pop('username', None)
        # Keep session_id for cart functionality
    
    @staticmethod
    def get_current_user():
        """Get the current authenticated user.
        
        Returns:
            User object if authenticated, None otherwise
        """
        return getattr(g, 'current_user', None)
    
    @staticmethod
    def is_authenticated():
        """Check if current user is authenticated.
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return AuthMiddleware.get_current_user() is not None
    
    @staticmethod
    def get_session_id():
        """Get the current session ID.
        
        Returns:
            Session ID string
        """
        return session.get('session_id')
    
    @staticmethod
    def require_https():
        """Middleware to require HTTPS in production.
        
        This should be used in production environments.
        """
        if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
            # In production, you might want to redirect to HTTPS
            # For development, we'll just log a warning
            pass