from datetime import datetime
from database import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func

class OrderStatus(db.Model):
    __tablename__ = 'order_statuses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __init__(self, name, description=None, is_active=True, sort_order=0):
        self.name = name.upper() if name else None
        self.description = description
        self.is_active = is_active
        self.sort_order = sort_order
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_active_statuses(cls):
        """Get all active order statuses ordered by sort_order"""
        return cls.query.filter_by(is_active=True).order_by(cls.sort_order).all()
    
    @classmethod
    def create_default_statuses(cls):
        """Create default order statuses if they don't exist"""
        default_statuses = [
            {'name': 'PENDING', 'description': 'Order received, awaiting confirmation', 'sort_order': 1},
            {'name': 'CONFIRMED', 'description': 'Order confirmed, preparing for processing', 'sort_order': 2},
            {'name': 'PROCESSING', 'description': 'Order is being processed', 'sort_order': 3},
            {'name': 'COMPLETED', 'description': 'Order completed successfully', 'sort_order': 4},
            {'name': 'CANCELLED', 'description': 'Order cancelled', 'sort_order': 5},
            {'name': 'REFUNDED', 'description': 'Order refunded', 'sort_order': 6}
        ]
        
        created_count = 0
        for status_data in default_statuses:
            existing = cls.query.filter_by(name=status_data['name']).first()
            if not existing:
                status = cls(
                    name=status_data['name'],
                    description=status_data['description'],
                    sort_order=status_data['sort_order']
                )
                db.session.add(status)
                created_count += 1
        
        if created_count > 0:
            db.session.commit()
        
        return created_count
    
    def __repr__(self):
        return f'<OrderStatus {self.name}>'