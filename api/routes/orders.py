from flask import Blueprint, request, jsonify, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from models.order import Order
from models.order_product import OrderProduct
from models.product import Product
from database import db
from models.order_status import OrderStatus
from utils.responses import success_response, error_response
from utils.validators import validate_required_fields

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    """Get orders - users see their own, admins see all"""
    try:
        # Get query parameters
        status_filter = request.args.get('status_id', type=int)
        limit = min(request.args.get('limit', 50, type=int), 100)  # Max 100
        offset = request.args.get('offset', 0, type=int)
        include_products = request.args.get('include_products', 'false').lower() == 'true'
        
        # Check if user is admin
        if hasattr(g.current_user, 'is_admin') and g.current_user.is_admin:
            orders = Order.get_all_orders(status_filter, limit, offset)
        else:
            orders = Order.get_user_orders(g.current_user.id, status_filter, limit, offset)
        
        return success_response(
            data={
                'orders': [order.to_dict(include_products=include_products) for order in orders],
                'count': len(orders),
                'limit': limit,
                'offset': offset
            },
            message="Orders retrieved successfully"
        )
        
    except Exception as e:
        return error_response(
            message="Failed to retrieve orders",
            status_code=500
        )

@orders_bp.route('/api/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get specific order details"""
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return error_response(
                message="Order not found",
                status_code=404
            )
        
        # Check if user can access this order
        if not (hasattr(g.current_user, 'is_admin') and g.current_user.is_admin) and order.user_id != g.current_user.id:
            return error_response(
                message="Access denied",
                status_code=403
            )
        
        include_products = request.args.get('include_products', 'true').lower() == 'true'
        include_user = request.args.get('include_user', 'false').lower() == 'true'
        
        return success_response(
            data=order.to_dict(include_products=include_products, include_user=include_user),
            message="Order retrieved successfully"
        )
        
    except Exception as e:
        return error_response(
            message="Failed to retrieve order",
            status_code=500
        )

@orders_bp.route('/api/orders', methods=['POST'])
@login_required
def create_order():
    """Create a new order from cart or direct products"""
    try:
        data = request.get_json()
        
        # Validate required fields
        validation_error = validate_required_fields(data, ['products'])
        if validation_error:
            return validation_error
        
        products_data = data.get('products', [])
        if not products_data:
            return error_response(
                message="At least one product is required",
                status_code=400
            )
        
        # Get default PENDING status
        pending_status = OrderStatus.query.filter_by(name='PENDING').first()
        if not pending_status:
            return error_response(
                message="Order status system not initialized",
                status_code=500
            )
        
        # Create new order
        order = Order(
            user_id=g.current_user.id,
            status_id=pending_status.id,
            notes=data.get('notes')
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Process each product
        total_amount = Decimal('0.00')
        
        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity', 1)
            
            if not product_id or quantity <= 0:
                db.session.rollback()
                return error_response(
                    message="Invalid product data",
                    status_code=400
                )
            
            # Get product and validate
            product = Product.query.get(product_id)
            if not product:
                db.session.rollback()
                return error_response(
                    message=f"Product {product_id} not found",
                    status_code=404
                )
            
            if not product.is_active:
                db.session.rollback()
                return error_response(
                    message=f"Product {product.name} is not available",
                    status_code=400
                )
            
            if product.stock_quantity < quantity:
                db.session.rollback()
                return error_response(
                    message=f"Insufficient stock for {product.name}. Available: {product.stock_quantity}",
                    status_code=400
                )
            
            # Create order product
            order_product = OrderProduct(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                product_description=product.description,
                quantity=quantity,
                unit_price=product.price
            )
            
            db.session.add(order_product)
            
            # Update product stock
            product.stock_quantity -= quantity
            
            total_amount += order_product.line_total
        
        # Update order totals
        order.subtotal = total_amount
        discount_amount = Decimal(str(data.get('discount_amount', 0)))
        order.discount_amount = discount_amount
        order.total_amount = total_amount - discount_amount
        
        db.session.commit()
        
        # Clear cart if specified
        if data.get('clear_cart', False):
            cart = Cart.query.filter_by(user_id=g.current_user.id).first()
            if cart:
                CartItem.query.filter_by(cart_id=cart.id).delete()
                db.session.commit()
        
        return success_response(
            data=order.to_dict(include_products=True),
            message="Order created successfully",
            status_code=201
        )
        
    except IntegrityError:
        db.session.rollback()
        return error_response(
            message="Order creation failed due to data conflict",
            status_code=409
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to create order",
            status_code=500
        )

@orders_bp.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@login_required
@admin_required
def update_order_status(order_id):
    """Update order status (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        validation_error = validate_required_fields(data, ['status_id'])
        if validation_error:
            return validation_error
        
        new_status_id = data.get('status_id')
        
        # Get order
        order = Order.query.get(order_id)
        if not order:
            return error_response(
                message="Order not found",
                status_code=404
            )
        
        # Validate new status exists
        new_status = OrderStatus.query.get(new_status_id)
        if not new_status:
            return error_response(
                message="Invalid status ID",
                status_code=400
            )
        
        if not new_status.is_active:
            return error_response(
                message="Cannot set order to inactive status",
                status_code=400
            )
        
        # Update order status
        old_status_id = order.status_id
        order.update_status(new_status_id)
        
        db.session.commit()
        
        return success_response(
            data={
                'order': order.to_dict(include_products=True),
                'old_status_id': old_status_id,
                'new_status_id': new_status_id
            },
            message=f"Order status updated to {new_status.name}"
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Failed to update order status",
            status_code=500
        )

@orders_bp.route('/api/orders/from-cart', methods=['POST'])
@login_required
def create_order_from_cart():
    """Create order from user's current cart"""
    try:
        data = request.get_json() or {}
        
        # Get user's cart
        cart = Cart.query.filter_by(user_id=g.current_user.id).first()
        if not cart:
            return error_response(
                message="No cart found",
                status_code=404
            )
        
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        if not cart_items:
            return error_response(
                message="Cart is empty",
                status_code=400
            )
        
        # Convert cart items to products data
        products_data = []
        for item in cart_items:
            products_data.append({
                'product_id': item.product_id,
                'quantity': item.quantity
            })
        
        # Create order data
        order_data = {
            'products': products_data,
            'notes': data.get('notes'),
            'discount_amount': data.get('discount_amount', 0),
            'clear_cart': True  # Always clear cart when creating from cart
        }
        
        # Use the existing create_order logic
        request._cached_json = order_data
        return create_order()
        
    except Exception as e:
        return error_response(
            message="Failed to create order from cart",
            status_code=500
        )