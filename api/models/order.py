from datetime import datetime
from decimal import Decimal
from database import db
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('order_statuses.id'), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False, default=0.00)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship('User', backref='orders')
    status = relationship('OrderStatus', backref='orders')
    order_products = relationship('OrderProduct', back_populates='order', cascade='all, delete-orphan')
    
    def __init__(self, user_id, status_id=None, subtotal=0.00, discount_amount=0.00, notes=None):
        self.user_id = user_id
        self.status_id = status_id
        self.subtotal = Decimal(str(subtotal))
        self.discount_amount = Decimal(str(discount_amount))
        self.total_amount = self.subtotal - self.discount_amount
        self.notes = notes
        self.order_number = self._generate_order_number()
    
    def _generate_order_number(self):
        """Generate unique order number in format ORD-YYYYMMDD-XXXXXXXX"""
        date_part = datetime.now().strftime('%Y%m%d')
        unique_part = str(uuid.uuid4()).replace('-', '')[:8].upper()
        return f'ORD-{date_part}-{unique_part}'
    
    def calculate_total(self):
        """Calculate and update total amount based on order products"""
        if self.order_products:
            self.subtotal = sum(op.line_total for op in self.order_products)
        else:
            self.subtotal = Decimal('0.00')
        
        self.total_amount = self.subtotal - self.discount_amount
        return self.total_amount
    
    def add_product(self, product, quantity, unit_price=None):
        """Add a product to this order"""
        from api.models.order_product import OrderProduct
        
        # Use current product price if not specified
        if unit_price is None:
            unit_price = product.price
        
        order_product = OrderProduct(
            order_id=self.id,
            product_id=product.id,
            product_name=product.name,
            product_description=product.description,
            quantity=quantity,
            unit_price=unit_price
        )
        
        self.order_products.append(order_product)
        self.calculate_total()
        return order_product
    
    def update_status(self, new_status_id):
        """Update order status and timestamp"""
        self.status_id = new_status_id
        self.updated_at = func.now()
    
    def to_dict(self, include_products=False, include_user=False):
        """Convert order to dictionary"""
        result = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'status_id': self.status_id,
            'status_name': self.status.name if self.status else None,
            'subtotal': float(self.subtotal),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_products and self.order_products:
            result['products'] = [op.to_dict() for op in self.order_products]
            result['product_count'] = len(self.order_products)
        
        if include_user and self.user:
            result['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email
            }
        
        return result
    
    @classmethod
    def get_user_orders(cls, user_id, status_filter=None, limit=50, offset=0):
        """Get orders for a specific user with optional filtering"""
        query = cls.query.filter_by(user_id=user_id)
        
        if status_filter:
            query = query.filter_by(status_id=status_filter)
        
        return query.order_by(cls.created_at.desc()).offset(offset).limit(limit).all()
    
    @classmethod
    def get_all_orders(cls, status_filter=None, limit=50, offset=0):
        """Get all orders (admin function) with optional filtering"""
        query = cls.query
        
        if status_filter:
            query = query.filter_by(status_id=status_filter)
        
        return query.order_by(cls.created_at.desc()).offset(offset).limit(limit).all()
    
    def __repr__(self):
        return f'<Order {self.order_number}>'