import pytest
import json
from app import create_app
from database import db
from models.user import User
from config import TestingConfig


class TestUsers:
    """Test cases for user CRUD endpoints."""
    
    @pytest.fixture
    def app(self):
        """Create and configure a test app."""
        app = create_app(TestingConfig)
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """Create a test client."""
        return app.test_client()
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
    
    @pytest.fixture
    def admin_user_data(self):
        """Sample admin user data for testing."""
        return {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'AdminPassword123!'
        }
    
    @pytest.fixture
    def registered_user(self, app, sample_user_data):
        """Create a registered user for testing."""
        with app.app_context():
            user = User(
                username=sample_user_data['username'],
                email=sample_user_data['email']
            )
            user.set_password(sample_user_data['password'])
            db.session.add(user)
            db.session.commit()
            return user
    
    @pytest.fixture
    def admin_user(self, app, admin_user_data):
        """Create an admin user for testing."""
        with app.app_context():
            user = User(
                username=admin_user_data['username'],
                email=admin_user_data['email']
            )
            user.set_password(admin_user_data['password'])
            db.session.add(user)
            db.session.commit()
            return user
    
    def login_user(self, client, username, password):
        """Helper method to login a user."""
        login_data = {
            'username': username,
            'password': password
        }
        return client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    def test_get_user_profile_success(self, client, registered_user, sample_user_data):
        """Test successful user profile retrieval."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Get user profile
        response = client.get(f'/api/users/{registered_user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['username'] == sample_user_data['username']
        assert data['user']['email'] == sample_user_data['email']
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_get_user_profile_not_authenticated(self, client, registered_user):
        """Test user profile retrieval without authentication."""
        response = client.get(f'/api/users/{registered_user.id}')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not authenticated' in data['error'].lower()
    
    def test_get_user_profile_unauthorized(self, client, registered_user, admin_user, admin_user_data):
        """Test user profile retrieval by different user (unauthorized)."""
        # Login as admin
        self.login_user(client, admin_user_data['username'], admin_user_data['password'])
        
        # Try to access different user's profile (should work for admin)
        response = client.get(f'/api/users/{registered_user.id}')
        
        assert response.status_code == 200  # Admin can access any profile
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_get_user_profile_not_found(self, client, sample_user_data):
        """Test user profile retrieval for non-existent user."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Try to get non-existent user
        response = client.get('/api/users/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not found' in data['error'].lower()
    
    def test_update_user_profile_success(self, client, registered_user, sample_user_data):
        """Test successful user profile update."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Update profile
        update_data = {
            'email': 'newemail@example.com'
        }
        response = client.put(f'/api/users/{registered_user.id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['user']['email'] == 'newemail@example.com'
        assert data['user']['username'] == sample_user_data['username']  # Unchanged
    
    def test_update_user_profile_not_authenticated(self, client, registered_user):
        """Test user profile update without authentication."""
        update_data = {'email': 'newemail@example.com'}
        response = client.put(f'/api/users/{registered_user.id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not authenticated' in data['error'].lower()
    
    def test_update_user_profile_invalid_email(self, client, registered_user, sample_user_data):
        """Test user profile update with invalid email."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Update with invalid email
        update_data = {
            'email': 'invalid-email'
        }
        response = client.put(f'/api/users/{registered_user.id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'email' in data['error'].lower()
    
    def test_delete_user_profile_success(self, client, registered_user, sample_user_data):
        """Test successful user profile deletion."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Delete profile
        response = client.delete(f'/api/users/{registered_user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'User account deleted successfully'
    
    def test_delete_user_profile_not_authenticated(self, client, registered_user):
        """Test user profile deletion without authentication."""
        response = client.delete(f'/api/users/{registered_user.id}')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not authenticated' in data['error'].lower()
    
    def test_change_password_success(self, client, registered_user, sample_user_data):
        """Test successful password change."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Change password
        password_data = {
            'current_password': sample_user_data['password'],
            'new_password': 'NewPassword123!'
        }
        response = client.put(f'/api/users/{registered_user.id}/password',
                             data=json.dumps(password_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'Password updated successfully'
    
    def test_change_password_wrong_current(self, client, registered_user, sample_user_data):
        """Test password change with wrong current password."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Change password with wrong current password
        password_data = {
            'current_password': 'WrongPassword123!',
            'new_password': 'NewPassword123!'
        }
        response = client.put(f'/api/users/{registered_user.id}/password',
                             data=json.dumps(password_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'current password' in data['error'].lower()
    
    def test_change_password_weak_new_password(self, client, registered_user, sample_user_data):
        """Test password change with weak new password."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Change password with weak new password
        password_data = {
            'current_password': sample_user_data['password'],
            'new_password': '123'  # Too weak
        }
        response = client.put(f'/api/users/{registered_user.id}/password',
                             data=json.dumps(password_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'password' in data['error'].lower()
    
    def test_get_current_user_profile(self, client, registered_user, sample_user_data):
        """Test getting current user's profile."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Get current user profile
        response = client.get('/api/users/me')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['username'] == sample_user_data['username']
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_update_current_user_profile(self, client, registered_user, sample_user_data):
        """Test updating current user's profile."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Update current user profile
        update_data = {
            'email': 'updated@example.com'
        }
        response = client.put('/api/users/me',
                             data=json.dumps(update_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['user']['email'] == 'updated@example.com'
    
    def test_delete_current_user_profile(self, client, registered_user, sample_user_data):
        """Test deleting current user's profile."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Delete current user profile
        response = client.delete('/api/users/me')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'User account deleted successfully'
    
    def test_change_current_user_password(self, client, registered_user, sample_user_data):
        """Test changing current user's password."""
        # Login first
        self.login_user(client, sample_user_data['username'], sample_user_data['password'])
        
        # Change current user password
        password_data = {
            'current_password': sample_user_data['password'],
            'new_password': 'NewPassword123!'
        }
        response = client.put('/api/users/me/password',
                             data=json.dumps(password_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'Password updated successfully'