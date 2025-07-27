from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database import db
from models.order_status import OrderStatus
from utils.responses import success_response, error_response
from utils.validators import validate_required_fields

order_statuses_bp = Blueprint('order_statuses', __name__)

@order_statuses_bp.route('/api/order-statuses', methods=['GET'])
def get_order_statuses():
    """Get all active order statuses ordered by sort_order"""
    try:
        statuses = OrderStatus.get_active_statuses()
        return success_response(
            data=[status.to_dict() for status in statuses],
            message="Order statuses retrieved successfully"
        )
    except Exception as e:
        return error_response(
            message="Failed to retrieve order statuses",
            status_code=500
        )

@order_statuses_bp.route('/api/order-statuses', methods=['POST'])
@login_required
@admin_required
def create_order_status():
    """Create a new order status (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        validation_error = validate_required_fields(data, ['name'])
        if validation_error:
            return validation_error
        
        # Validate field lengths
        name = data.get('name', '').strip()
        description = data.get('description', '').strip() if data.get('description') else None
        
        if len(name) > 50:
            return error_response(
                message="Status name must be 50 characters or less",
                status_code=400
            )
        
        if description and len(description) > 200:
            return error_response(
                message="Status description must be 200 characters or less",
                status_code=400
            )
        
        # Create new order status
        order_status = OrderStatus(
            name=name,
            description=description,
            is_active=data.get('is_active', True),
            sort_order=data.get('sort_order', 0)
        )
        
        db.session.add(order_status)
        db.session.commit()
        
        return success_response(
            data=order_status.to_dict(),
            message="Order status created successfully",
            status_code=201
        )
        
    except IntegrityError:
        db.session.rollback()
        return error_response(
            message="Order status with this name already exists",
            status_code=409
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to create order status",
            status_code=500
        )

@order_statuses_bp.route('/api/order-statuses/seed', methods=['POST'])
@login_required
@admin_required
def seed_order_statuses():
    """Initialize default order statuses (admin only)"""
    try:
        created_count = OrderStatus.create_default_statuses()
        
        if created_count > 0:
            return success_response(
                data={'created_count': created_count},
                message=f"Successfully created {created_count} default order statuses",
                status_code=201
            )
        else:
            return success_response(
                data={'created_count': 0},
                message="Default order statuses already exist"
            )
            
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to seed order statuses",
            status_code=500
        )