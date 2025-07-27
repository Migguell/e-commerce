"""Test configuration and fixtures for pytest."""

import pytest
import os
import tempfile
from decimal import Decimal
from flask import Flask
from api.app import create_app
from api.database import db, init_db
from api.models.product import Product, Category
from api.models.cart import CartItem

@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Test configuration
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    }
    
    # Create app with test config
    app = create_app(test_config)
    
    # Create application context
    with app.app_context():
        # Initialize database
        init_db()
        yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='function')
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Create test runner."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        # Clear all tables
        db.drop_all()
        db.create_all()
        
        yield db.session
        
        # Cleanup after test
        db.session.rollback()
        db.drop_all()

@pytest.fixture
def sample_category(db_session):
    """Create a sample category for testing."""
    category = Category(
        name="Electronics",
        description="Electronic devices and accessories"
    )
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def sample_product(db_session, sample_category):
    """Create a sample product for testing."""
    product = Product(
        name="Test Product",
        description="A test product for unit testing",
        price=Decimal('29.99'),
        image_url="https://example.com/test-product.jpg",
        category_id=sample_category.id,
        stock_quantity=10
    )
    db_session.add(product)
    db_session.commit()
    return product

@pytest.fixture
def multiple_products(db_session, sample_category):
    """Create multiple products for testing."""
    products = []
    
    # Create another category
    books_category = Category(
        name="Books",
        description="Books and literature"
    )
    db_session.add(books_category)
    db_session.commit()
    
    # Create products in different categories
    product_data = [
        {
            'name': 'Smartphone',
            'description': 'Latest smartphone with advanced features',
            'price': Decimal('699.99'),
            'category_id': sample_category.id,
            'stock_quantity': 5
        },
        {
            'name': 'Laptop',
            'description': 'High-performance laptop for professionals',
            'price': Decimal('1299.99'),
            'category_id': sample_category.id,
            'stock_quantity': 3
        },
        {
            'name': 'Python Programming Book',
            'description': 'Learn Python programming from scratch',
            'price': Decimal('39.99'),
            'category_id': books_category.id,
            'stock_quantity': 15
        },
        {
            'name': 'Wireless Headphones',
            'description': 'Premium wireless headphones with noise cancellation',
            'price': Decimal('199.99'),
            'category_id': sample_category.id,
            'stock_quantity': 8
        }
    ]
    
    for data in product_data:
        product = Product(**data)
        db_session.add(product)
        products.append(product)
    
    db_session.commit()
    return products

@pytest.fixture
def sample_cart_item(db_session, sample_product):
    """Create a sample cart item for testing."""
    cart_item = CartItem(
        session_id="test-session-123",
        product_id=sample_product.id,
        quantity=2
    )
    db_session.add(cart_item)
    db_session.commit()
    return cart_item

@pytest.fixture
def sample_cart_items(db_session, multiple_products):
    """Create multiple cart items for testing."""
    cart_items = []
    session_id = "test-session-456"
    
    # Add first 3 products to cart
    for i, product in enumerate(multiple_products[:3]):
        cart_item = CartItem(
            session_id=session_id,
            product_id=product.id,
            quantity=i + 1  # 1, 2, 3 quantities
        )
        db_session.add(cart_item)
        cart_items.append(cart_item)
    
    db_session.commit()
    return cart_items

@pytest.fixture
def valid_product_data():
    """Valid product data for testing."""
    return {
        'name': 'Test Product',
        'description': 'A product for testing',
        'price': '49.99',
        'image_url': 'https://example.com/product.jpg',
        'stock_quantity': 20
    }

@pytest.fixture
def valid_category_data():
    """Valid category data for testing."""
    return {
        'name': 'Test Category',
        'description': 'A category for testing'
    }

@pytest.fixture
def valid_cart_item_data(sample_product):
    """Valid cart item data for testing."""
    return {
        'product_id': sample_product.id,
        'quantity': 3
    }

@pytest.fixture
def api_headers():
    """Common API headers for testing."""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

@pytest.fixture
def session_id():
    """Test session ID."""
    return "test-session-789"