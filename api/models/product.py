from datetime import datetime
from decimal import Decimal
from database import db
from utils.validators import validate_string_length, validate_positive_number

class Product(db.Model):
    """Product model for e-commerce catalog."""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with category (back_populates for better control)
    category = db.relationship('Category', back_populates='products')
    
    # Relationship with cart items
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, name, price, category_id, description=None, stock_quantity=0, image_url=None):
        # Validation
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        
        validate_string_length(name, 'name', max_length=200)
        validate_positive_number(price, 'price')
        validate_positive_number(stock_quantity, 'stock_quantity', allow_zero=True)
        
        if description:
            validate_string_length(description, 'description', max_length=1000)
        
        if image_url:
            validate_string_length(image_url, 'image_url', max_length=500)
        
        # Assignment
        self.name = name.strip()
        self.description = description.strip() if description else None
        self.price = Decimal(str(price))
        self.stock_quantity = int(stock_quantity)
        self.category_id = int(category_id)
        self.image_url = image_url.strip() if image_url else None
    
    def to_dict(self, include_category=False):
        """Convert product to dictionary for JSON serialization"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock_quantity': self.stock_quantity,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_category and self.category:
            result['category'] = self.category.to_dict()
        
        return result
    
    def update_stock(self, quantity_change):
        """Update stock quantity with validation"""
        new_quantity = self.stock_quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        self.stock_quantity = new_quantity
    
    def is_in_stock(self, quantity=1):
        """Check if product has sufficient stock"""
        return self.stock_quantity >= quantity and self.is_active
    
    def __repr__(self):
        return f'<Product {self.name}>'