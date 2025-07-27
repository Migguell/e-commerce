from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from models.product import Product, Category
from database import db
from utils.responses import success_response, error_response
from utils.validators import validate_product_data
from utils.exceptions import ValidationError, NotFoundError

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering and search.
    
    Query Parameters:
    - category_id: Filter by category ID
    - category: Filter by category name
    - search: Search in product name and description
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - in_stock: Filter by stock availability (true/false)
    - page: Page number for pagination (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - sort_by: Sort field (name, price, created_at)
    - sort_order: Sort order (asc, desc)
    """
    try:
        # Get query parameters
        category_id = request.args.get('category_id', type=int)
        category_name = request.args.get('category')
        search_term = request.args.get('search', '').strip()
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        in_stock = request.args.get('in_stock')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = Product.query
        
        # Apply filters
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if category_name:
            category = Category.query.filter(Category.name.ilike(f'%{category_name}%')).first()
            if category:
                query = query.filter(Product.category_id == category.id)
        
        if search_term:
            search_filter = or_(
                Product.name.ilike(f'%{search_term}%'),
                Product.description.ilike(f'%{search_term}%')
            )
            query = query.filter(search_filter)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if in_stock is not None:
            if in_stock.lower() == 'true':
                query = query.filter(Product.stock_quantity > 0)
            elif in_stock.lower() == 'false':
                query = query.filter(Product.stock_quantity == 0)
        
        # Apply sorting
        if sort_by in ['name', 'price', 'created_at', 'stock_quantity']:
            sort_column = getattr(Product, sort_by)
            if sort_order.lower() == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Execute paginated query
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        products = pagination.items
        
        # Prepare response data
        products_data = [product.to_dict() for product in products]
        
        response_data = {
            'products': products_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'filters_applied': {
                'category_id': category_id,
                'category': category_name,
                'search': search_term,
                'min_price': min_price,
                'max_price': max_price,
                'in_stock': in_stock
            }
        }
        
        return success_response(response_data, "Products retrieved successfully")
        
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve products: {str(e)}")

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID."""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")
        
        return success_response(product.to_dict(), "Product retrieved successfully")
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve product: {str(e)}")

@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product (Admin functionality)."""
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must contain JSON data")
        
        # Validate product data
        validated_data = validate_product_data(data)
        
        # Check if category exists
        if validated_data.get('category_id'):
            category = Category.query.get(validated_data['category_id'])
            if not category:
                raise ValidationError(f"Category with ID {validated_data['category_id']} not found")
        
        # Create new product
        product = Product(
            name=validated_data['name'],
            description=validated_data.get('description'),
            price=validated_data['price'],
            image_url=validated_data.get('image_url'),
            category_id=validated_data.get('category_id'),
            stock_quantity=validated_data.get('stock_quantity', 0)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return success_response(product.to_dict(), "Product created successfully", status_code=201)
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to create product: {str(e)}")

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product (Admin functionality)."""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")
        
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must contain JSON data")
        
        # Validate product data
        validated_data = validate_product_data(data, partial=True)
        
        # Check if category exists (if provided)
        if 'category_id' in validated_data and validated_data['category_id']:
            category = Category.query.get(validated_data['category_id'])
            if not category:
                raise ValidationError(f"Category with ID {validated_data['category_id']} not found")
        
        # Update product fields
        for field, value in validated_data.items():
            setattr(product, field, value)
        
        db.session.commit()
        
        return success_response(product.to_dict(), "Product updated successfully")
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to update product: {str(e)}")

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product (Admin functionality)."""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")
        
        db.session.delete(product)
        db.session.commit()
        
        return success_response(None, "Product deleted successfully")
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to delete product: {str(e)}")