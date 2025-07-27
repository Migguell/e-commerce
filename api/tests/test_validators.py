"""Unit tests for validation utilities."""

import pytest
from decimal import Decimal
from api.utils.validators import (
    validate_product_data,
    validate_cart_item_data,
    validate_category_data,
    validate_session_id,
    validate_pagination_params
)
from api.utils.exceptions import ValidationError

class TestProductValidation:
    """Test cases for product data validation."""
    
    def test_valid_product_data(self):
        """Test validation of valid product data."""
        data = {
            'name': 'Test Product',
            'description': 'A great test product',
            'price': '29.99',
            'image_url': 'https://example.com/product.jpg',
            'category_id': 1,
            'stock_quantity': 10
        }
        
        validated = validate_product_data(data)
        
        assert validated['name'] == 'Test Product'
        assert validated['description'] == 'A great test product'
        assert validated['price'] == Decimal('29.99')
        assert validated['image_url'] == 'https://example.com/product.jpg'
        assert validated['category_id'] == 1
        assert validated['stock_quantity'] == 10
    
    def test_minimal_product_data(self):
        """Test validation of minimal required product data."""
        data = {
            'name': 'Minimal Product',
            'price': 19.99
        }
        
        validated = validate_product_data(data)
        
        assert validated['name'] == 'Minimal Product'
        assert validated['price'] == Decimal('19.99')
    
    def test_partial_product_update(self):
        """Test validation for partial product updates."""
        data = {
            'name': 'Updated Name',
            'price': '39.99'
        }
        
        validated = validate_product_data(data, partial=True)
        
        assert validated['name'] == 'Updated Name'
        assert validated['price'] == Decimal('39.99')
        assert 'description' not in validated
    
    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        # Missing name
        with pytest.raises(ValidationError, match="Product name is required"):
            validate_product_data({'price': 29.99})
        
        # Missing price
        with pytest.raises(ValidationError, match="Price is required"):
            validate_product_data({'name': 'Test Product'})
    
    def test_invalid_name(self):
        """Test validation of invalid product names."""
        base_data = {'price': 29.99}
        
        # Empty name
        with pytest.raises(ValidationError, match="Product name cannot be empty"):
            validate_product_data({**base_data, 'name': ''})
        
        # Non-string name
        with pytest.raises(ValidationError, match="Product name must be a string"):
            validate_product_data({**base_data, 'name': 123})
        
        # Too long name
        long_name = 'x' * 256
        with pytest.raises(ValidationError, match="Product name cannot exceed 255 characters"):
            validate_product_data({**base_data, 'name': long_name})
    
    def test_invalid_price(self):
        """Test validation of invalid prices."""
        base_data = {'name': 'Test Product'}
        
        # Negative price
        with pytest.raises(ValidationError, match="Price must be a positive number"):
            validate_product_data({**base_data, 'price': -10})
        
        # Zero price
        with pytest.raises(ValidationError, match="Price must be a positive number"):
            validate_product_data({**base_data, 'price': 0})
        
        # Invalid string price
        with pytest.raises(ValidationError, match="Price must be a valid number"):
            validate_product_data({**base_data, 'price': 'invalid'})
        
        # Too many decimal places
        with pytest.raises(ValidationError, match="Price cannot have more than 2 decimal places"):
            validate_product_data({**base_data, 'price': '29.999'})
        
        # Price too large
        with pytest.raises(ValidationError, match="Price cannot exceed 99,999,999.99"):
            validate_product_data({**base_data, 'price': '100000000'})
    
    def test_invalid_description(self):
        """Test validation of invalid descriptions."""
        base_data = {'name': 'Test Product', 'price': 29.99}
        
        # Non-string description
        with pytest.raises(ValidationError, match="Product description must be a string"):
            validate_product_data({**base_data, 'description': 123})
        
        # Too long description
        long_desc = 'x' * 5001
        with pytest.raises(ValidationError, match="Product description cannot exceed 5000 characters"):
            validate_product_data({**base_data, 'description': long_desc})
    
    def test_invalid_image_url(self):
        """Test validation of invalid image URLs."""
        base_data = {'name': 'Test Product', 'price': 29.99}
        
        # Non-string URL
        with pytest.raises(ValidationError, match="Image URL must be a string"):
            validate_product_data({**base_data, 'image_url': 123})
        
        # Invalid URL format
        with pytest.raises(ValidationError, match="Image URL must be a valid HTTP/HTTPS URL"):
            validate_product_data({**base_data, 'image_url': 'not-a-url'})
        
        # Too long URL
        long_url = 'https://example.com/' + 'x' * 500
        with pytest.raises(ValidationError, match="Image URL cannot exceed 500 characters"):
            validate_product_data({**base_data, 'image_url': long_url})
    
    def test_invalid_category_id(self):
        """Test validation of invalid category IDs."""
        base_data = {'name': 'Test Product', 'price': 29.99}
        
        # Non-integer category ID
        with pytest.raises(ValidationError, match="Category ID must be a positive integer"):
            validate_product_data({**base_data, 'category_id': 'invalid'})
        
        # Negative category ID
        with pytest.raises(ValidationError, match="Category ID must be a positive integer"):
            validate_product_data({**base_data, 'category_id': -1})
    
    def test_invalid_stock_quantity(self):
        """Test validation of invalid stock quantities."""
        base_data = {'name': 'Test Product', 'price': 29.99}
        
        # Non-integer stock
        with pytest.raises(ValidationError, match="Stock quantity must be a non-negative integer"):
            validate_product_data({**base_data, 'stock_quantity': 'invalid'})
        
        # Negative stock
        with pytest.raises(ValidationError, match="Stock quantity must be a non-negative integer"):
            validate_product_data({**base_data, 'stock_quantity': -1})
        
        # Too large stock
        with pytest.raises(ValidationError, match="Stock quantity cannot exceed 999,999"):
            validate_product_data({**base_data, 'stock_quantity': 1000000})

class TestCartItemValidation:
    """Test cases for cart item data validation."""
    
    def test_valid_cart_item_data(self):
        """Test validation of valid cart item data."""
        data = {
            'product_id': 1,
            'quantity': 3
        }
        
        validated = validate_cart_item_data(data)
        
        assert validated['product_id'] == 1
        assert validated['quantity'] == 3
    
    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        # Missing product_id
        with pytest.raises(ValidationError, match="Product ID is required"):
            validate_cart_item_data({'quantity': 1})
        
        # Missing quantity
        with pytest.raises(ValidationError, match="Quantity is required"):
            validate_cart_item_data({'product_id': 1})
    
    def test_invalid_product_id(self):
        """Test validation of invalid product IDs."""
        base_data = {'quantity': 1}
        
        # Non-integer product ID
        with pytest.raises(ValidationError, match="Product ID must be a positive integer"):
            validate_cart_item_data({**base_data, 'product_id': 'invalid'})
        
        # Negative product ID
        with pytest.raises(ValidationError, match="Product ID must be a positive integer"):
            validate_cart_item_data({**base_data, 'product_id': -1})
        
        # Zero product ID
        with pytest.raises(ValidationError, match="Product ID must be a positive integer"):
            validate_cart_item_data({**base_data, 'product_id': 0})
    
    def test_invalid_quantity(self):
        """Test validation of invalid quantities."""
        base_data = {'product_id': 1}
        
        # Non-integer quantity
        with pytest.raises(ValidationError, match="Quantity must be a positive integer"):
            validate_cart_item_data({**base_data, 'quantity': 'invalid'})
        
        # Negative quantity
        with pytest.raises(ValidationError, match="Quantity must be a positive integer"):
            validate_cart_item_data({**base_data, 'quantity': -1})
        
        # Zero quantity
        with pytest.raises(ValidationError, match="Quantity must be a positive integer"):
            validate_cart_item_data({**base_data, 'quantity': 0})
        
        # Too large quantity
        with pytest.raises(ValidationError, match="Quantity cannot exceed 999"):
            validate_cart_item_data({**base_data, 'quantity': 1000})

class TestCategoryValidation:
    """Test cases for category data validation."""
    
    def test_valid_category_data(self):
        """Test validation of valid category data."""
        data = {
            'name': 'Test Category',
            'description': 'A test category'
        }
        
        validated = validate_category_data(data)
        
        assert validated['name'] == 'Test Category'
        assert validated['description'] == 'A test category'
    
    def test_minimal_category_data(self):
        """Test validation of minimal category data."""
        data = {'name': 'Minimal Category'}
        
        validated = validate_category_data(data)
        
        assert validated['name'] == 'Minimal Category'
    
    def test_partial_category_update(self):
        """Test validation for partial category updates."""
        data = {'description': 'Updated description'}
        
        validated = validate_category_data(data, partial=True)
        
        assert validated['description'] == 'Updated description'
        assert 'name' not in validated
    
    def test_missing_required_name(self):
        """Test validation fails for missing name."""
        with pytest.raises(ValidationError, match="Category name is required"):
            validate_category_data({'description': 'No name'})
    
    def test_invalid_name(self):
        """Test validation of invalid category names."""
        # Empty name
        with pytest.raises(ValidationError, match="Category name cannot be empty"):
            validate_category_data({'name': ''})
        
        # Non-string name
        with pytest.raises(ValidationError, match="Category name must be a string"):
            validate_category_data({'name': 123})
        
        # Too long name
        long_name = 'x' * 101
        with pytest.raises(ValidationError, match="Category name cannot exceed 100 characters"):
            validate_category_data({'name': long_name})
        
        # Invalid characters
        with pytest.raises(ValidationError, match="Category name can only contain"):
            validate_category_data({'name': 'Invalid@Name!'})
    
    def test_invalid_description(self):
        """Test validation of invalid descriptions."""
        base_data = {'name': 'Test Category'}
        
        # Non-string description
        with pytest.raises(ValidationError, match="Category description must be a string"):
            validate_category_data({**base_data, 'description': 123})
        
        # Too long description
        long_desc = 'x' * 1001
        with pytest.raises(ValidationError, match="Category description cannot exceed 1000 characters"):
            validate_category_data({**base_data, 'description': long_desc})

class TestSessionIdValidation:
    """Test cases for session ID validation."""
    
    def test_valid_session_id(self):
        """Test validation of valid session IDs."""
        valid_ids = [
            'session-123',
            'user_session_456',
            'ABC123DEF456',
            'simple-session'
        ]
        
        for session_id in valid_ids:
            validated = validate_session_id(session_id)
            assert validated == session_id
    
    def test_invalid_session_id(self):
        """Test validation of invalid session IDs."""
        # Empty session ID
        with pytest.raises(ValidationError, match="Session ID cannot be empty"):
            validate_session_id('')
        
        # None session ID
        with pytest.raises(ValidationError, match="Session ID cannot be empty"):
            validate_session_id(None)
        
        # Non-string session ID
        with pytest.raises(ValidationError, match="Session ID must be a string"):
            validate_session_id(123)
        
        # Too long session ID
        long_id = 'x' * 256
        with pytest.raises(ValidationError, match="Session ID cannot exceed 255 characters"):
            validate_session_id(long_id)
        
        # Invalid characters
        with pytest.raises(ValidationError, match="Session ID can only contain"):
            validate_session_id('invalid@session!')

class TestPaginationValidation:
    """Test cases for pagination parameter validation."""
    
    def test_valid_pagination_params(self):
        """Test validation of valid pagination parameters."""
        page, per_page = validate_pagination_params(1, 10)
        assert page == 1
        assert per_page == 10
        
        page, per_page = validate_pagination_params(5, 50)
        assert page == 5
        assert per_page == 50
    
    def test_invalid_page(self):
        """Test validation of invalid page numbers."""
        # Non-integer page
        with pytest.raises(ValidationError, match="Page must be a positive integer"):
            validate_pagination_params('invalid', 10)
        
        # Negative page
        with pytest.raises(ValidationError, match="Page must be a positive integer"):
            validate_pagination_params(-1, 10)
        
        # Zero page
        with pytest.raises(ValidationError, match="Page must be a positive integer"):
            validate_pagination_params(0, 10)
    
    def test_invalid_per_page(self):
        """Test validation of invalid per_page values."""
        # Non-integer per_page
        with pytest.raises(ValidationError, match="Per page must be a positive integer"):
            validate_pagination_params(1, 'invalid')
        
        # Negative per_page
        with pytest.raises(ValidationError, match="Per page must be a positive integer"):
            validate_pagination_params(1, -1)
        
        # Zero per_page
        with pytest.raises(ValidationError, match="Per page must be a positive integer"):
            validate_pagination_params(1, 0)
        
        # Too large per_page
        with pytest.raises(ValidationError, match="Per page cannot exceed 100"):
            validate_pagination_params(1, 101)
    
    def test_custom_max_per_page(self):
        """Test validation with custom max_per_page limit."""
        # Should pass with custom limit
        page, per_page = validate_pagination_params(1, 150, max_per_page=200)
        assert page == 1
        assert per_page == 150
        
        # Should fail with custom limit
        with pytest.raises(ValidationError, match="Per page cannot exceed 50"):
            validate_pagination_params(1, 75, max_per_page=50)