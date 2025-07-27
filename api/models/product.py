from datetime import datetime
from database import db
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

class Category(db.Model):
    """Category model for product categorization."""
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    
    # Relationship with products
    products = relationship('Product', back_populates='category', lazy='dynamic')
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate category name."""
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")
        if len(name.strip()) > 100:
            raise ValueError("Category name cannot exceed 100 characters")
        return name.strip()
    
    def to_dict(self):
        """Convert category to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': self.products.count()
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    """Product model for e-commerce catalog."""
    
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String(500))
    category_id = Column(Integer, ForeignKey('categories.id'))
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    category = relationship('Category', back_populates='products')
    cart_items = relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate product name."""
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        if len(name.strip()) > 255:
            raise ValueError("Product name cannot exceed 255 characters")
        return name.strip()
    
    @validates('price')
    def validate_price(self, key, price):
        """Validate product price."""
        if price is None:
            raise ValueError("Price cannot be None")
        if float(price) <= 0:
            raise ValueError("Price must be a positive number")
        if float(price) > 99999999.99:
            raise ValueError("Price cannot exceed 99,999,999.99")
        return price
    
    @validates('stock_quantity')
    def validate_stock_quantity(self, key, stock_quantity):
        """Validate stock quantity."""
        if stock_quantity is None:
            return 0
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        return stock_quantity
    
    @validates('image_url')
    def validate_image_url(self, key, image_url):
        """Validate image URL."""
        if image_url and len(image_url) > 500:
            raise ValueError("Image URL cannot exceed 500 characters")
        return image_url
    
    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0
    
    @property
    def formatted_price(self):
        """Get formatted price as string."""
        return f"${float(self.price):.2f}"
    
    def to_dict(self, include_category=True):
        """Convert product to dictionary for JSON serialization."""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'formatted_price': self.formatted_price,
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity,
            'is_in_stock': self.is_in_stock,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_category and self.category:
            result['category'] = {
                'id': self.category.id,
                'name': self.category.name
            }
        else:
            result['category_id'] = self.category_id
        
        return result
    
    def __repr__(self):
        return f'<Product {self.name} - ${self.price}>'