from decimal import Decimal
from database import db
from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship

class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product_name = Column(String(255), nullable=False)  # Snapshot at order time
    product_description = Column(Text, nullable=True)   # Snapshot at order time
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Price at order time
    line_total = Column(Numeric(10, 2), nullable=False)  # Calculated field
    
    # Relationships
    order = relationship('Order', back_populates='order_products')
    product = relationship('Product', backref='order_products')
    
    def __init__(self, order_id, product_id, product_name, quantity, unit_price, product_description=None):
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.quantity = int(quantity)
        self.unit_price = Decimal(str(unit_price))
        self.line_total = self.quantity * self.unit_price
    
    def update_quantity(self, new_quantity):
        """Update quantity and recalculate line total"""
        self.quantity = int(new_quantity)
        self.line_total = self.quantity * self.unit_price
        return self.line_total
    
    def update_unit_price(self, new_price):
        """Update unit price and recalculate line total"""
        self.unit_price = Decimal(str(new_price))
        self.line_total = self.quantity * self.unit_price
        return self.line_total
    
    def to_dict(self, include_product_details=False):
        """Convert order product to dictionary"""
        result = {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_description': self.product_description,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'line_total': float(self.line_total)
        }
        
        if include_product_details and self.product:
            result['current_product'] = {
                'id': self.product.id,
                'name': self.product.name,
                'current_price': float(self.product.price),
                'stock_quantity': self.product.stock_quantity,
                'is_active': self.product.is_active
            }
        
        return result
    
    @property
    def total_value(self):
        """Alias for line_total for backward compatibility"""
        return self.line_total
    
    def __repr__(self):
        return f'<OrderProduct {self.product_name} x{self.quantity}>'