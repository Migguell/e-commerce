"""Unit tests for database models."""

import pytest
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from api.models.product import Product, Category
from api.models.cart import CartItem
from api.database import db

class TestCategory:
    """Test cases for Category model."""
    
    def test_create_category(self, db_session):
        """Test creating a new category."""
        category = Category(
            name="Test Category",
            description="A test category"
        )
        db_session.add(category)
        db_session.commit()
        
        assert category.id is not None
        assert category.name == "Test Category"
        assert category.description == "A test category"
        assert category.created_at is not None
        assert category.updated_at is not None
    
    def test_category_without_description(self, db_session):
        """Test creating category without description."""
        category = Category(name="Minimal Category")
        db_session.add(category)
        db_session.commit()
        
        assert category.id is not None
        assert category.name == "Minimal Category"
        assert category.description is None
    
    def test_category_name_required(self, db_session):
        """Test that category name is required."""
        category = Category(description="No name category")
        db_session.add(category)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_category_name_unique(self, db_session):
        """Test that category names must be unique."""
        category1 = Category(name="Unique Name")
        category2 = Category(name="Unique Name")
        
        db_session.add(category1)
        db_session.commit()
        
        db_session.add(category2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_category_to_dict(self, sample_category):
        """Test category serialization to dictionary."""
        category_dict = sample_category.to_dict()
        
        assert 'id' in category_dict
        assert 'name' in category_dict
        assert 'description' in category_dict
        assert 'created_at' in category_dict
        assert 'updated_at' in category_dict
        assert category_dict['name'] == sample_category.name
    
    def test_category_to_dict_with_products(self, db_session, sample_category):
        """Test category serialization with products included."""
        # Add a product to the category
        product = Product(
            name="Test Product",
            price=Decimal('19.99'),
            category_id=sample_category.id
        )
        db_session.add(product)
        db_session.commit()
        
        category_dict = sample_category.to_dict(include_products=True)
        
        assert 'products' in category_dict
        assert len(category_dict['products']) == 1
        assert category_dict['products'][0]['name'] == "Test Product"

class TestProduct:
    """Test cases for Product model."""
    
    def test_create_product(self, db_session, sample_category):
        """Test creating a new product."""
        product = Product(
            name="Test Product",
            description="A test product",
            price=Decimal('29.99'),
            image_url="https://example.com/product.jpg",
            category_id=sample_category.id,
            stock_quantity=10
        )
        db_session.add(product)
        db_session.commit()
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == Decimal('29.99')
        assert product.stock_quantity == 10
        assert product.category_id == sample_category.id
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_product_minimal_fields(self, db_session):
        """Test creating product with only required fields."""
        product = Product(
            name="Minimal Product",
            price=Decimal('9.99')
        )
        db_session.add(product)
        db_session.commit()
        
        assert product.id is not None
        assert product.name == "Minimal Product"
        assert product.price == Decimal('9.99')
        assert product.description is None
        assert product.image_url is None
        assert product.category_id is None
        assert product.stock_quantity == 0  # Default value
    
    def test_product_name_required(self, db_session):
        """Test that product name is required."""
        product = Product(price=Decimal('19.99'))
        db_session.add(product)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_product_price_required(self, db_session):
        """Test that product price is required."""
        product = Product(name="No Price Product")
        db_session.add(product)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_product_category_relationship(self, sample_product, sample_category):
        """Test product-category relationship."""
        assert sample_product.category is not None
        assert sample_product.category.id == sample_category.id
        assert sample_product.category.name == sample_category.name
    
    def test_product_to_dict(self, sample_product):
        """Test product serialization to dictionary."""
        product_dict = sample_product.to_dict()
        
        required_fields = [
            'id', 'name', 'description', 'price', 'image_url',
            'category_id', 'stock_quantity', 'created_at', 'updated_at'
        ]
        
        for field in required_fields:
            assert field in product_dict
        
        assert product_dict['name'] == sample_product.name
        assert str(product_dict['price']) == str(sample_product.price)
    
    def test_product_to_dict_with_category(self, sample_product):
        """Test product serialization with category included."""
        product_dict = sample_product.to_dict(include_category=True)
        
        assert 'category' in product_dict
        assert product_dict['category']['name'] == sample_product.category.name
    
    def test_product_is_in_stock(self, db_session):
        """Test product stock availability check."""
        # Product with stock
        in_stock_product = Product(
            name="In Stock Product",
            price=Decimal('19.99'),
            stock_quantity=5
        )
        
        # Product without stock
        out_of_stock_product = Product(
            name="Out of Stock Product",
            price=Decimal('29.99'),
            stock_quantity=0
        )
        
        db_session.add_all([in_stock_product, out_of_stock_product])
        db_session.commit()
        
        assert in_stock_product.is_in_stock() is True
        assert out_of_stock_product.is_in_stock() is False
    
    def test_product_has_sufficient_stock(self, sample_product):
        """Test product stock sufficiency check."""
        # Sample product has 10 in stock
        assert sample_product.has_sufficient_stock(5) is True
        assert sample_product.has_sufficient_stock(10) is True
        assert sample_product.has_sufficient_stock(15) is False
        assert sample_product.has_sufficient_stock(0) is True

class TestCartItem:
    """Test cases for CartItem model."""
    
    def test_create_cart_item(self, db_session, sample_product):
        """Test creating a new cart item."""
        cart_item = CartItem(
            session_id="test-session",
            product_id=sample_product.id,
            quantity=3
        )
        db_session.add(cart_item)
        db_session.commit()
        
        assert cart_item.id is not None
        assert cart_item.session_id == "test-session"
        assert cart_item.product_id == sample_product.id
        assert cart_item.quantity == 3
        assert cart_item.created_at is not None
        assert cart_item.updated_at is not None
    
    def test_cart_item_session_id_required(self, db_session, sample_product):
        """Test that session_id is required."""
        cart_item = CartItem(
            product_id=sample_product.id,
            quantity=1
        )
        db_session.add(cart_item)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_cart_item_product_id_required(self, db_session):
        """Test that product_id is required."""
        cart_item = CartItem(
            session_id="test-session",
            quantity=1
        )
        db_session.add(cart_item)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_cart_item_unique_constraint(self, db_session, sample_product):
        """Test unique constraint on session_id and product_id."""
        cart_item1 = CartItem(
            session_id="test-session",
            product_id=sample_product.id,
            quantity=1
        )
        cart_item2 = CartItem(
            session_id="test-session",
            product_id=sample_product.id,
            quantity=2
        )
        
        db_session.add(cart_item1)
        db_session.commit()
        
        db_session.add(cart_item2)
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_cart_item_product_relationship(self, sample_cart_item, sample_product):
        """Test cart item-product relationship."""
        assert sample_cart_item.product is not None
        assert sample_cart_item.product.id == sample_product.id
        assert sample_cart_item.product.name == sample_product.name
    
    def test_cart_item_subtotal(self, sample_cart_item, sample_product):
        """Test cart item subtotal calculation."""
        # sample_cart_item has quantity 2, sample_product price is 29.99
        expected_subtotal = Decimal('29.99') * 2
        assert sample_cart_item.subtotal == expected_subtotal
    
    def test_cart_item_to_dict(self, sample_cart_item):
        """Test cart item serialization to dictionary."""
        cart_dict = sample_cart_item.to_dict()
        
        required_fields = [
            'id', 'session_id', 'product_id', 'quantity',
            'subtotal', 'created_at', 'updated_at'
        ]
        
        for field in required_fields:
            assert field in cart_dict
        
        assert cart_dict['session_id'] == sample_cart_item.session_id
        assert cart_dict['quantity'] == sample_cart_item.quantity
    
    def test_cart_item_to_dict_with_product(self, sample_cart_item):
        """Test cart item serialization with product included."""
        cart_dict = sample_cart_item.to_dict(include_product=True)
        
        assert 'product' in cart_dict
        assert cart_dict['product']['name'] == sample_cart_item.product.name
    
    def test_get_cart_total(self, db_session, sample_cart_items):
        """Test getting total for a cart session."""
        session_id = "test-session-456"
        total = CartItem.get_cart_total(session_id)
        
        # Calculate expected total from sample_cart_items fixture
        # Products have prices: 699.99, 1299.99, 39.99
        # Quantities: 1, 2, 3
        expected_total = (Decimal('699.99') * 1 + 
                         Decimal('1299.99') * 2 + 
                         Decimal('39.99') * 3)
        
        assert total == expected_total
    
    def test_get_cart_item_count(self, sample_cart_items):
        """Test getting item count for a cart session."""
        session_id = "test-session-456"
        count = CartItem.get_cart_item_count(session_id)
        
        # sample_cart_items has quantities: 1, 2, 3
        expected_count = 1 + 2 + 3
        assert count == expected_count
    
    def test_get_cart_summary(self, sample_cart_items):
        """Test getting cart summary for a session."""
        session_id = "test-session-456"
        summary = CartItem.get_cart_summary(session_id)
        
        assert 'total_amount' in summary
        assert 'total_items' in summary
        assert 'item_count' in summary
        assert 'items' in summary
        
        assert summary['item_count'] == 3  # 3 different products
        assert summary['total_items'] == 6  # 1+2+3 quantities
        assert len(summary['items']) == 3
    
    def test_empty_cart_summary(self, db_session):
        """Test cart summary for empty cart."""
        summary = CartItem.get_cart_summary("empty-session")
        
        assert summary['total_amount'] == Decimal('0')
        assert summary['total_items'] == 0
        assert summary['item_count'] == 0
        assert summary['items'] == []