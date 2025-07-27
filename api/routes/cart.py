from flask import Blueprint, request, jsonify
from api.models.cart import Cart, CartItem
from api.models.product import Product
from api.database import db
from utils.responses import success_response, error_response
from utils.validators import validate_cart_item_data
from utils.exceptions import ValidationError, NotFoundError
from sqlalchemy.exc import IntegrityError

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/<session_id>', methods=['GET'])
def get_cart(session_id):
    """Get cart contents for a specific session."""
    try:
        if not session_id or not session_id.strip():
            raise ValidationError("Session ID cannot be empty")
        
        # Get cart summary with all items
        cart_summary = CartItem.get_cart_summary(session_id)
        
        return success_response(cart_summary, "Cart retrieved successfully")
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve cart: {str(e)}")

@cart_bp.route('/cart/<session_id>/items', methods=['POST'])
def add_to_cart(session_id):
    """Add an item to the cart or update quantity if item already exists."""
    try:
        if not session_id or not session_id.strip():
            raise ValidationError("Session ID cannot be empty")
        
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must contain JSON data")
        
        # Validate cart item data
        validated_data = validate_cart_item_data(data)
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        
        # Check if product exists and is in stock
        product = Product.query.get(product_id)
        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")
        
        if product.stock_quantity < quantity:
            raise ValidationError(f"Insufficient stock. Available: {product.stock_quantity}, Requested: {quantity}")
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            session_id=session_id,
            product_id=product_id
        ).first()
        
        if existing_item:
            # Update existing item quantity
            new_quantity = existing_item.quantity + quantity
            
            if product.stock_quantity < new_quantity:
                raise ValidationError(f"Insufficient stock. Available: {product.stock_quantity}, Total requested: {new_quantity}")
            
            existing_item.quantity = new_quantity
            db.session.commit()
            
            return success_response(
                existing_item.to_dict(),
                "Cart item quantity updated successfully"
            )
        else:
            # Create new cart item
            cart_item = CartItem(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity
            )
            
            db.session.add(cart_item)
            db.session.commit()
            
            return success_response(
                cart_item.to_dict(),
                "Item added to cart successfully",
                status_code=201
            )
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except IntegrityError as e:
        db.session.rollback()
        return error_response("INTEGRITY_ERROR", "Database constraint violation", status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to add item to cart: {str(e)}")

@cart_bp.route('/cart/<session_id>/items/<int:item_id>', methods=['PUT'])
def update_cart_item(session_id, item_id):
    """Update the quantity of a specific cart item."""
    try:
        if not session_id or not session_id.strip():
            raise ValidationError("Session ID cannot be empty")
        
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must contain JSON data")
        
        if 'quantity' not in data:
            raise ValidationError("Quantity is required")
        
        quantity = data['quantity']
        
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("Quantity must be a positive integer")
        
        if quantity > 999:
            raise ValidationError("Quantity cannot exceed 999")
        
        # Find cart item
        cart_item = CartItem.query.filter_by(
            id=item_id,
            session_id=session_id
        ).first()
        
        if not cart_item:
            raise NotFoundError(f"Cart item with ID {item_id} not found in session {session_id}")
        
        # Check stock availability
        if cart_item.product.stock_quantity < quantity:
            raise ValidationError(f"Insufficient stock. Available: {cart_item.product.stock_quantity}, Requested: {quantity}")
        
        # Update quantity
        cart_item.quantity = quantity
        db.session.commit()
        
        return success_response(
            cart_item.to_dict(),
            "Cart item updated successfully"
        )
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to update cart item: {str(e)}")

@cart_bp.route('/cart/<session_id>/items/<int:item_id>', methods=['DELETE'])
def remove_cart_item(session_id, item_id):
    """Remove a specific item from the cart."""
    try:
        if not session_id or not session_id.strip():
            raise ValidationError("Session ID cannot be empty")
        
        # Find cart item
        cart_item = CartItem.query.filter_by(
            id=item_id,
            session_id=session_id
        ).first()
        
        if not cart_item:
            raise NotFoundError(f"Cart item with ID {item_id} not found in session {session_id}")
        
        # Remove item
        db.session.delete(cart_item)
        db.session.commit()
        
        return success_response(None, "Item removed from cart successfully")
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to remove cart item: {str(e)}")

@cart_bp.route('/cart/<session_id>', methods=['DELETE'])
def clear_cart(session_id):
    """Clear all items from the cart for a specific session."""
    try:
        if not session_id or not session_id.strip():
            raise ValidationError("Session ID cannot be empty")
        
        # Get all cart items for the session
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            return success_response(None, "Cart is already empty")
        
        # Delete all items
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        
        return success_response(None, f"Cart cleared successfully. Removed {len(cart_items)} items.")
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to clear cart: {str(e)}")

@cart_bp.route('/cart/<session_id>/summary', methods=['GET'])
def get_cart_summary(session_id):
    """Get cart summary with totals and item counts."""
    try:
        if not session_id or not session_id.strip():
            raise ValidationError("Session ID cannot be empty")
        
        # Get cart summary
        cart_summary = CartItem.get_cart_summary(session_id)
        
        # Add additional summary information
        summary_data = {
            'session_id': session_id,
            'total_amount': cart_summary['total_amount'],
            'formatted_total': cart_summary['formatted_total'],
            'total_items': cart_summary['total_items'],
            'unique_products': cart_summary['unique_products'],
            'is_empty': cart_summary['total_items'] == 0
        }
        
        return success_response(summary_data, "Cart summary retrieved successfully")
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve cart summary: {str(e)}")