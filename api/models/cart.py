from datetime import datetime
from database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

class CartItem(db.Model):
    """CartItem model for shopping cart functionality."""
    
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    product = relationship('Product', back_populates='cart_items')
    
    # Unique constraint to prevent duplicate items in same session
    __table_args__ = (
        UniqueConstraint('session_id', 'product_id', name='unique_session_product'),
    )
    
    @validates('session_id')
    def validate_session_id(self, key, session_id):
        """Validate session ID."""
        if not session_id or not session_id.strip():
            raise ValueError("Session ID cannot be empty")
        if len(session_id.strip()) > 255:
            raise ValueError("Session ID cannot exceed 255 characters")
        return session_id.strip()
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
        """Validate cart item quantity."""
        if quantity is None:
            raise ValueError("Quantity cannot be None")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if quantity > 999:
            raise ValueError("Quantity cannot exceed 999")
        return quantity
    
    @property
    def subtotal(self):
        """Calculate subtotal for this cart item."""
        if self.product and self.product.price:
            return float(self.product.price) * self.quantity
        return 0.0
    
    @property
    def formatted_subtotal(self):
        """Get formatted subtotal as string."""
        return f"${self.subtotal:.2f}"
    
    def to_dict(self, include_product=True):
        """Convert cart item to dictionary for JSON serialization."""
        result = {
            'id': self.id,
            'session_id': self.session_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
            'formatted_subtotal': self.formatted_subtotal,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_product and self.product:
            result['product'] = {
                'id': self.product.id,
                'name': self.product.name,
                'price': float(self.product.price),
                'formatted_price': self.product.formatted_price,
                'image_url': self.product.image_url,
                'stock_quantity': self.product.stock_quantity,
                'is_in_stock': self.product.is_in_stock
            }
        
        return result
    
    @classmethod
    def get_cart_total(cls, session_id):
        """Calculate total amount for all items in a cart session."""
        cart_items = cls.query.filter_by(session_id=session_id).all()
        total = sum(item.subtotal for item in cart_items)
        return total
    
    @classmethod
    def get_cart_item_count(cls, session_id):
        """Get total number of items in a cart session."""
        cart_items = cls.query.filter_by(session_id=session_id).all()
        total_items = sum(item.quantity for item in cart_items)
        return total_items
    
    @classmethod
    def get_cart_summary(cls, session_id):
        """Get cart summary with totals and item count."""
        cart_items = cls.query.filter_by(session_id=session_id).all()
        
        total_amount = sum(item.subtotal for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        unique_products = len(cart_items)
        
        return {
            'session_id': session_id,
            'total_amount': total_amount,
            'formatted_total': f"${total_amount:.2f}",
            'total_items': total_items,
            'unique_products': unique_products,
            'items': [item.to_dict() for item in cart_items]
        }
    
    def __repr__(self):
        return f'<CartItem {self.session_id} - Product {self.product_id} x{self.quantity}>'