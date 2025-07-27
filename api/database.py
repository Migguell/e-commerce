from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Configure logging for database operations
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log SQL execution time for performance monitoring."""
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log SQL execution completion and duration."""
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > 0.05:  # Log slow queries (>50ms)
        logging.warning(f"Slow query detected: {total:.4f}s - {statement[:100]}...")

def init_database(app):
    """Initialize database with application context."""
    with app.app_context():
        # Import models to ensure tables are created
        from api.models.category import Category
        from api.models.product import Product
        from api.models.cart import Cart, CartItem
        from api.models.user import User
        from api.models.order_status import OrderStatus
        from api.models.order import Order
        from api.models.order_product import OrderProduct
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")

def reset_database(app):
    """Reset database - WARNING: This will delete all data!"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset completed!")