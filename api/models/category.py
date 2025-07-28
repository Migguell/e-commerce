from datetime import datetime
from database import db
from utils.validators import validate_string_length

class Category(db.Model):
    """Category model for product categorization."""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with products (back_populates for better control)
    products = db.relationship('Product', back_populates='category', lazy=True)
    
    def __init__(self, name, description=None):
        if not name or not name.strip():
            raise ValueError("Category name cannot be empty")
        
        validate_string_length(name, 'name', max_length=100)
        
        self.name = name.strip()
        self.description = description.strip() if description else None
    
    def to_dict(self, include_products=False):
        """Convert category to dictionary for JSON serialization"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': len(self.products) if self.products else 0
        }
        
        if include_products:
            result['products'] = [product.to_dict() for product in self.products]
        
        return result
    
    def __repr__(self):
        return f'<Category {self.name}>'