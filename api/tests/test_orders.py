import pytest
import json
from datetime import datetime
from api.app import create_app
from api.database import db
from api.models.user import User
from api.models.product import Product
from api.models.category import Category
from api.models.order import Order
from api.models.order_product import OrderProduct
from api.models.order_status import OrderStatus
from api.models.cart import Cart
from api.models.cart_item import CartItem


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        
        # Create default order statuses
        OrderStatus.create_default_statuses()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return session."""
    # Create test user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    # Register user
    client.post('/api/auth/register', 
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Login user
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    return {}


@pytest.fixture
def admin_headers(client):
    """Create admin user and return session."""
    # Create admin user
    admin_data = {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'adminpass123',
        'first_name': 'Admin',
        'last_name': 'User'
    }
    
    # Register admin
    client.post('/api/auth/register',
                data=json.dumps(admin_data),
                content_type='application/json')
    
    # Make user admin
    with client.application.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        admin_user.is_admin = True
        db.session.commit()
    
    # Login admin
    login_data = {
        'username': 'admin',
        'password': 'adminpass123'
    }
    
    response = client.post('/api/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    return {}


@pytest.fixture
def sample_products(client):
    """Create sample products for testing."""
    with client.application.app_context():
        # Create category
        category = Category(
            name='Electronics',
            description='Electronic products'
        )
        db.session.add(category)
        db.session.flush()
        
        # Create products
        products = [
            Product(
                name='Laptop',
                description='Gaming laptop',
                price=999.99,
                stock_quantity=10,
                category_id=category.id,
                is_active=True
            ),
            Product(
                name='Mouse',
                description='Wireless mouse',
                price=29.99,
                stock_quantity=50,
                category_id=category.id,
                is_active=True
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        return [p.id for p in products]


class TestOrderRoutes:
    """Test order management routes."""
    
    def test_get_orders_unauthorized(self, client):
        """Test getting orders without authentication."""
        response = client.get('/api/orders')
        assert response.status_code == 401
    
    def test_get_orders_empty(self, client, auth_headers):
        """Test getting orders when none exist."""
        response = client.get('/api/orders')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data'] == []
    
    def test_create_order_success(self, client, auth_headers, sample_products):
        """Test creating an order successfully."""
        order_data = {
            'products': [
                {
                    'product_id': sample_products[0],
                    'quantity': 2
                },
                {
                    'product_id': sample_products[1],
                    'quantity': 1
                }
            ],
            'notes': 'Test order'
        }
        
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'order_number' in data['data']
        assert len(data['data']['products']) == 2
    
    def test_create_order_invalid_product(self, client, auth_headers):
        """Test creating order with invalid product."""
        order_data = {
            'products': [
                {
                    'product_id': 999,
                    'quantity': 1
                }
            ]
        }
        
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              content_type='application/json')
        
        assert response.status_code == 404
    
    def test_create_order_insufficient_stock(self, client, auth_headers, sample_products):
        """Test creating order with insufficient stock."""
        order_data = {
            'products': [
                {
                    'product_id': sample_products[0],
                    'quantity': 100  # More than available stock
                }
            ]
        }
        
        response = client.post('/api/orders',
                              data=json.dumps(order_data),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_get_order_by_id(self, client, auth_headers, sample_products):
        """Test getting specific order by ID."""
        # First create an order
        order_data = {
            'products': [
                {
                    'product_id': sample_products[0],
                    'quantity': 1
                }
            ]
        }
        
        create_response = client.post('/api/orders',
                                     data=json.dumps(order_data),
                                     content_type='application/json')
        
        order_id = json.loads(create_response.data)['data']['id']
        
        # Get the order
        response = client.get(f'/api/orders/{order_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == order_id
    
    def test_get_nonexistent_order(self, client, auth_headers):
        """Test getting non-existent order."""
        response = client.get('/api/orders/999')
        assert response.status_code == 404
    
    def test_update_order_status_admin(self, client, admin_headers, sample_products):
        """Test updating order status as admin."""
        # Create order first
        with client.application.app_context():
            user = User.query.filter_by(username='admin').first()
            order = Order(
                user_id=user.id,
                status_id=1,  # Pending
                subtotal=100.00,
                total_amount=100.00
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id
        
        # Update status
        status_data = {'status_id': 2}  # Processing
        
        response = client.put(f'/api/orders/{order_id}/status',
                             data=json.dumps(status_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_update_order_status_non_admin(self, client, auth_headers):
        """Test updating order status as non-admin user."""
        status_data = {'status_id': 2}
        
        response = client.put('/api/orders/1/status',
                             data=json.dumps(status_data),
                             content_type='application/json')
        
        assert response.status_code == 403
    
    def test_create_order_from_cart(self, client, auth_headers, sample_products):
        """Test creating order from cart."""
        # Add items to cart first
        with client.application.app_context():
            user = User.query.filter_by(username='testuser').first()
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.flush()
            
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=sample_products[0],
                quantity=2
            )
            db.session.add(cart_item)
            db.session.commit()
        
        # Create order from cart
        response = client.post('/api/orders/from-cart',
                              data=json.dumps({'clear_cart': True}),
                              content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['products']) == 1
    
    def test_create_order_from_empty_cart(self, client, auth_headers):
        """Test creating order from empty cart."""
        response = client.post('/api/orders/from-cart',
                              content_type='application/json')
        
        assert response.status_code == 400


class TestOrderModel:
    """Test Order model functionality."""
    
    def test_order_creation(self, app):
        """Test creating an order."""
        with app.app_context():
            # Create user
            user = User(
                username='testuser',
                email='test@example.com',
                password_hash='hashed_password'
            )
            db.session.add(user)
            db.session.flush()
            
            # Create order
            order = Order(
                user_id=user.id,
                status_id=1,
                subtotal=100.00,
                total_amount=100.00
            )
            db.session.add(order)
            db.session.commit()
            
            assert order.id is not None
            assert order.order_number is not None
            assert order.user_id == user.id
    
    def test_order_number_generation(self, app):
        """Test order number generation."""
        with app.app_context():
            order = Order(
                user_id=1,
                status_id=1,
                subtotal=50.00,
                total_amount=50.00
            )
            
            order_number = order.generate_order_number()
            assert order_number.startswith('ORD-')
            assert len(order_number) == 17  # ORD- + 13 characters
    
    def test_calculate_totals(self, app):
        """Test order total calculation."""
        with app.app_context():
            order = Order(
                user_id=1,
                status_id=1,
                subtotal=100.00,
                discount_amount=10.00,
                total_amount=0.00  # Will be calculated
            )
            
            order.calculate_totals()
            assert order.total_amount == 90.00
    
    def test_order_to_dict(self, app):
        """Test order dictionary conversion."""
        with app.app_context():
            order = Order(
                user_id=1,
                status_id=1,
                subtotal=100.00,
                total_amount=100.00
            )
            db.session.add(order)
            db.session.commit()
            
            order_dict = order.to_dict()
            
            assert 'id' in order_dict
            assert 'order_number' in order_dict
            assert 'user_id' in order_dict
            assert 'status_id' in order_dict
            assert 'subtotal' in order_dict
            assert 'total_amount' in order_dict
            assert 'created_at' in order_dict


class TestOrderProductModel:
    """Test OrderProduct model functionality."""
    
    def test_order_product_creation(self, app):
        """Test creating an order product."""
        with app.app_context():
            order_product = OrderProduct(
                order_id=1,
                product_id=1,
                product_name='Test Product',
                quantity=2,
                unit_price=50.00
            )
            
            assert order_product.line_total == 100.00
    
    def test_update_quantity(self, app):
        """Test updating order product quantity."""
        with app.app_context():
            order_product = OrderProduct(
                order_id=1,
                product_id=1,
                product_name='Test Product',
                quantity=2,
                unit_price=50.00
            )
            
            order_product.update_quantity(3)
            assert order_product.quantity == 3
            assert order_product.line_total == 150.00
    
    def test_update_unit_price(self, app):
        """Test updating order product unit price."""
        with app.app_context():
            order_product = OrderProduct(
                order_id=1,
                product_id=1,
                product_name='Test Product',
                quantity=2,
                unit_price=50.00
            )
            
            order_product.update_unit_price(60.00)
            assert order_product.unit_price == 60.00
            assert order_product.line_total == 120.00
    
    def test_order_product_to_dict(self, app):
        """Test order product dictionary conversion."""
        with app.app_context():
            order_product = OrderProduct(
                order_id=1,
                product_id=1,
                product_name='Test Product',
                quantity=2,
                unit_price=50.00
            )
            
            product_dict = order_product.to_dict()
            
            assert 'id' in product_dict
            assert 'order_id' in product_dict
            assert 'product_id' in product_dict
            assert 'product_name' in product_dict
            assert 'quantity' in product_dict
            assert 'unit_price' in product_dict
            assert 'line_total' in product_dict