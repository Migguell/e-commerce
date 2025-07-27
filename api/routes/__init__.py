"""Routes package for the e-commerce backend API.

This package contains all Flask blueprints for API endpoints:
- auth: User authentication endpoints (register, login, logout)
- users: User profile management endpoints
- products: Product catalog and search endpoints
- cart: Shopping cart management endpoints
- categories: Product category endpoints
"""

from .auth import auth_bp
from .users import users_bp
from .products import products_bp
from .cart import cart_bp
from .categories import categories_bp

__all__ = ['auth_bp', 'users_bp', 'products_bp', 'cart_bp', 'categories_bp']