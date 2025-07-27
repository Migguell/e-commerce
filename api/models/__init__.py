"""Models package for the e-commerce backend API.

This package contains all SQLAlchemy models for the application:
- User: User authentication and management
- Product: Product catalog management
- Category: Product categorization
- CartItem: Shopping cart functionality
"""

from .user import User
from .product import Product, Category
from .cart import CartItem

__all__ = ['User', 'Product', 'Category', 'CartItem']