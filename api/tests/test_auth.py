import pytest
import json
from app import create_app
from database import db
from models.user import User
from config import TestingConfig


class TestAuth:
    """Test cases for authentication endpoints."""
    
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
    
    def test_register_success(self, client, sample_user_data):
        """Test successful user registration."""
        response = client.post('/api/auth/register', 
                             data=json.dumps(sample_user_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'User registered successfully'
        assert 'user' in data
        assert data['user']['username'] == sample_user_data['username']
        assert data['user']['email'] == sample_user_data['email']
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields."""
        incomplete_data = {'username': 'testuser'}
        response = client.post('/api/auth/register',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        invalid_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'TestPassword123!'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'email' in data['error'].lower()
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        weak_password_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123'  # Too short and weak
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(weak_password_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'password' in data['error'].lower()
    
    def test_register_duplicate_username(self, client, registered_user, sample_user_data):
        """Test registration with duplicate username."""
        duplicate_data = {
            'username': sample_user_data['username'],  # Same username
            'email': 'different@example.com',
            'password': 'TestPassword123!'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(duplicate_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'username' in data['error'].lower()
    
    def test_register_duplicate_email(self, client, registered_user, sample_user_data):
        """Test registration with duplicate email."""
        duplicate_data = {
            'username': 'differentuser',
            'email': sample_user_data['email'],  # Same email
            'password': 'TestPassword123!'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(duplicate_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'email' in data['error'].lower()
    
    def test_login_success(self, client, registered_user, sample_user_data):
        """Test successful user login."""
        login_data = {
            'username': sample_user_data['username'],
            'password': sample_user_data['password']
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'Login successful'
        assert 'user' in data
        assert data['user']['username'] == sample_user_data['username']
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username."""
        login_data = {
            'username': 'nonexistent',
            'password': 'TestPassword123!'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'invalid' in data['error'].lower()
    
    def test_login_invalid_password(self, client, registered_user, sample_user_data):
        """Test login with invalid password."""
        login_data = {
            'username': sample_user_data['username'],
            'password': 'WrongPassword123!'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'invalid' in data['error'].lower()
    
    def test_login_missing_fields(self, client):
        """Test login with missing required fields."""
        incomplete_data = {'username': 'testuser'}
        response = client.post('/api/auth/login',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_logout_success(self, client, registered_user, sample_user_data):
        """Test successful user logout."""
        # First login
        login_data = {
            'username': sample_user_data['username'],
            'password': sample_user_data['password']
        }
        client.post('/api/auth/login',
                   data=json.dumps(login_data),
                   content_type='application/json')
        
        # Then logout
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['message'] == 'Logout successful'
    
    def test_logout_not_authenticated(self, client):
        """Test logout when not authenticated."""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not authenticated' in data['error'].lower()
    
    def test_current_user_authenticated(self, client, registered_user, sample_user_data):
        """Test getting current user when authenticated."""
        # First login
        login_data = {
            'username': sample_user_data['username'],
            'password': sample_user_data['password']
        }
        client.post('/api/auth/login',
                   data=json.dumps(login_data),
                   content_type='application/json')
        
        # Get current user
        response = client.get('/api/auth/me')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['username'] == sample_user_data['username']
        assert 'password' not in data['user']
        assert 'password_hash' not in data['user']
    
    def test_current_user_not_authenticated(self, client):
        """Test getting current user when not authenticated."""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'not authenticated' in data['error'].lower()
    
    def test_auth_status_authenticated(self, client, registered_user, sample_user_data):
        """Test authentication status when authenticated."""
        # First login
        login_data = {
            'username': sample_user_data['username'],
            'password': sample_user_data['password']
        }
        client.post('/api/auth/login',
                   data=json.dumps(login_data),
                   content_type='application/json')
        
        # Check auth status
        response = client.get('/api/auth/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['authenticated'] is True
        assert 'session_id' in data
    
    def test_auth_status_not_authenticated(self, client):
        """Test authentication status when not authenticated."""
        response = client.get('/api/auth/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['authenticated'] is False
        assert data['session_id'] is None