"""Input validation functions for API endpoints."""

import re
from decimal import Decimal, InvalidOperation
from .exceptions import ValidationError

def validate_product_data(data, partial=False):
    """Validate product data for create/update operations.
    
    Args:
        data (dict): Product data to validate
        partial (bool): If True, allows partial updates (not all fields required)
    
    Returns:
        dict: Validated and cleaned data
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Data must be a dictionary")
    
    validated = {}
    
    # Name validation
    if 'name' in data:
        name = data['name']
        if not isinstance(name, str):
            raise ValidationError("Product name must be a string")
        name = name.strip()
        if not name:
            raise ValidationError("Product name cannot be empty")
        if len(name) > 255:
            raise ValidationError("Product name cannot exceed 255 characters")
        validated['name'] = name
    elif not partial:
        raise ValidationError("Product name is required")
    
    # Description validation
    if 'description' in data:
        description = data['description']
        if description is not None:
            if not isinstance(description, str):
                raise ValidationError("Product description must be a string")
            description = description.strip()
            if len(description) > 5000:
                raise ValidationError("Product description cannot exceed 5000 characters")
            validated['description'] = description if description else None
        else:
            validated['description'] = None
    
    # Price validation
    if 'price' in data:
        price = data['price']
        if price is None:
            raise ValidationError("Price cannot be null")
        
        try:
            # Convert to Decimal for precise validation
            if isinstance(price, str):
                price_decimal = Decimal(price)
            else:
                price_decimal = Decimal(str(price))
            
            if price_decimal <= 0:
                raise ValidationError("Price must be a positive number")
            
            if price_decimal > Decimal('99999999.99'):
                raise ValidationError("Price cannot exceed 99,999,999.99")
            
            # Check decimal places
            if price_decimal.as_tuple().exponent < -2:
                raise ValidationError("Price cannot have more than 2 decimal places")
            
            validated['price'] = price_decimal
            
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError("Price must be a valid number")
    elif not partial:
        raise ValidationError("Price is required")
    
    # Image URL validation
    if 'image_url' in data:
        image_url = data['image_url']
        if image_url is not None:
            if not isinstance(image_url, str):
                raise ValidationError("Image URL must be a string")
            image_url = image_url.strip()
            if len(image_url) > 500:
                raise ValidationError("Image URL cannot exceed 500 characters")
            
            # Basic URL format validation
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain...
                r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # host...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            if image_url and not url_pattern.match(image_url):
                raise ValidationError("Image URL must be a valid HTTP/HTTPS URL")
            
            validated['image_url'] = image_url if image_url else None
        else:
            validated['image_url'] = None
    
    # Category ID validation
    if 'category_id' in data:
        category_id = data['category_id']
        if category_id is not None:
            if not isinstance(category_id, int) or category_id <= 0:
                raise ValidationError("Category ID must be a positive integer")
            validated['category_id'] = category_id
        else:
            validated['category_id'] = None
    
    # Stock quantity validation
    if 'stock_quantity' in data:
        stock_quantity = data['stock_quantity']
        if stock_quantity is not None:
            if not isinstance(stock_quantity, int) or stock_quantity < 0:
                raise ValidationError("Stock quantity must be a non-negative integer")
            if stock_quantity > 999999:
                raise ValidationError("Stock quantity cannot exceed 999,999")
            validated['stock_quantity'] = stock_quantity
        else:
            validated['stock_quantity'] = 0
    
    return validated

def validate_cart_item_data(data):
    """Validate cart item data for add/update operations.
    
    Args:
        data (dict): Cart item data to validate
    
    Returns:
        dict: Validated and cleaned data
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Data must be a dictionary")
    
    validated = {}
    
    # Product ID validation
    if 'product_id' not in data:
        raise ValidationError("Product ID is required")
    
    product_id = data['product_id']
    if not isinstance(product_id, int) or product_id <= 0:
        raise ValidationError("Product ID must be a positive integer")
    validated['product_id'] = product_id
    
    # Quantity validation
    if 'quantity' not in data:
        raise ValidationError("Quantity is required")
    
    quantity = data['quantity']
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValidationError("Quantity must be a positive integer")
    
    if quantity > 999:
        raise ValidationError("Quantity cannot exceed 999")
    
    validated['quantity'] = quantity
    
    return validated

def validate_category_data(data, partial=False):
    """Validate category data for create/update operations.
    
    Args:
        data (dict): Category data to validate
        partial (bool): If True, allows partial updates (not all fields required)
    
    Returns:
        dict: Validated and cleaned data
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValidationError("Data must be a dictionary")
    
    validated = {}
    
    # Name validation
    if 'name' in data:
        name = data['name']
        if not isinstance(name, str):
            raise ValidationError("Category name must be a string")
        name = name.strip()
        if not name:
            raise ValidationError("Category name cannot be empty")
        if len(name) > 100:
            raise ValidationError("Category name cannot exceed 100 characters")
        
        # Check for valid characters (alphanumeric, spaces, hyphens, underscores)
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            raise ValidationError("Category name can only contain letters, numbers, spaces, hyphens, and underscores")
        
        validated['name'] = name
    elif not partial:
        raise ValidationError("Category name is required")
    
    # Description validation
    if 'description' in data:
        description = data['description']
        if description is not None:
            if not isinstance(description, str):
                raise ValidationError("Category description must be a string")
            description = description.strip()
            if len(description) > 1000:
                raise ValidationError("Category description cannot exceed 1000 characters")
            validated['description'] = description if description else None
        else:
            validated['description'] = None
    
    return validated

def validate_session_id(session_id):
    """Validate session ID format.
    
    Args:
        session_id (str): Session ID to validate
    
    Returns:
        str: Validated session ID
    
    Raises:
        ValidationError: If validation fails
    """
    if not session_id:
        raise ValidationError("Session ID cannot be empty")
    
    if not isinstance(session_id, str):
        raise ValidationError("Session ID must be a string")
    
    session_id = session_id.strip()
    
    if not session_id:
        raise ValidationError("Session ID cannot be empty")
    
    if len(session_id) > 255:
        raise ValidationError("Session ID cannot exceed 255 characters")
    
    # Basic format validation (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9\-_]+$', session_id):
        raise ValidationError("Session ID can only contain letters, numbers, hyphens, and underscores")
    
    return session_id

def validate_pagination_params(page, per_page, max_per_page=100):
    """Validate pagination parameters.
    
    Args:
        page (int): Page number
        per_page (int): Items per page
        max_per_page (int): Maximum allowed items per page
    
    Returns:
        tuple: Validated (page, per_page)
    
    Raises:
        ValidationError: If validation fails
    """
    # Page validation
    if not isinstance(page, int) or page < 1:
        raise ValidationError("Page must be a positive integer")
    
    # Per page validation
    if not isinstance(per_page, int) or per_page < 1:
        raise ValidationError("Per page must be a positive integer")
    
    if per_page > max_per_page:
        raise ValidationError(f"Per page cannot exceed {max_per_page}")
    
    return page, per_page