from flask import Blueprint, request, jsonify
from models.category import Category
from models.product import Product
from database import db
from utils.responses import success_response, error_response
from utils.validators import validate_category_data
from utils.exceptions import ValidationError, NotFoundError
from sqlalchemy.exc import IntegrityError

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories.
    
    Query Parameters:
    - include_products: Include product count for each category (true/false)
    - sort_by: Sort field (name, created_at, product_count)
    - sort_order: Sort order (asc, desc)
    """
    try:
        # Get query parameters
        include_products = request.args.get('include_products', 'true').lower() == 'true'
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc')
        
        # Build query
        query = Category.query
        
        # Apply sorting
        if sort_by in ['name', 'created_at']:
            sort_column = getattr(Category, sort_by)
            if sort_order.lower() == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        
        # Execute query
        categories = query.all()
        
        # Prepare response data
        categories_data = []
        for category in categories:
            category_dict = category.to_dict()
            if not include_products:
                category_dict.pop('product_count', None)
            categories_data.append(category_dict)
        
        # Sort by product count if requested
        if sort_by == 'product_count':
            reverse_order = sort_order.lower() == 'desc'
            categories_data.sort(key=lambda x: x.get('product_count', 0), reverse=reverse_order)
        
        response_data = {
            'categories': categories_data,
            'total_categories': len(categories_data)
        }
        
        return success_response(response_data, "Categories retrieved successfully")
        
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve categories: {str(e)}")

@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category by ID.
    
    Query Parameters:
    - include_products: Include products in this category (true/false)
    """
    try:
        include_products = request.args.get('include_products', 'false').lower() == 'true'
        
        category = Category.query.get(category_id)
        
        if not category:
            raise NotFoundError(f"Category with ID {category_id} not found")
        
        category_data = category.to_dict()
        
        if include_products:
            products = category.products.all()
            category_data['products'] = [product.to_dict(include_category=False) for product in products]
        
        return success_response(category_data, "Category retrieved successfully")
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve category: {str(e)}")

@categories_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new category (Admin functionality)."""
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must contain JSON data")
        
        # Validate category data
        validated_data = validate_category_data(data)
        
        # Check if category name already exists
        existing_category = Category.query.filter_by(name=validated_data['name']).first()
        if existing_category:
            raise ValidationError(f"Category with name '{validated_data['name']}' already exists")
        
        # Create new category
        category = Category(
            name=validated_data['name'],
            description=validated_data.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return success_response(category.to_dict(), "Category created successfully", status_code=201)
        
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except IntegrityError as e:
        db.session.rollback()
        return error_response("INTEGRITY_ERROR", "Category name must be unique", status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to create category: {str(e)}")

@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update an existing category (Admin functionality)."""
    try:
        category = Category.query.get(category_id)
        
        if not category:
            raise NotFoundError(f"Category with ID {category_id} not found")
        
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must contain JSON data")
        
        # Validate category data
        validated_data = validate_category_data(data, partial=True)
        
        # Check if new name conflicts with existing category
        if 'name' in validated_data:
            existing_category = Category.query.filter(
                Category.name == validated_data['name'],
                Category.id != category_id
            ).first()
            
            if existing_category:
                raise ValidationError(f"Category with name '{validated_data['name']}' already exists")
        
        # Update category fields
        for field, value in validated_data.items():
            setattr(category, field, value)
        
        db.session.commit()
        
        return success_response(category.to_dict(), "Category updated successfully")
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except IntegrityError as e:
        db.session.rollback()
        return error_response("INTEGRITY_ERROR", "Category name must be unique", status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to update category: {str(e)}")

@categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category (Admin functionality).
    
    Note: This will fail if there are products associated with this category.
    Use force=true query parameter to delete category and reassign products to null category.
    """
    try:
        force = request.args.get('force', 'false').lower() == 'true'
        
        category = Category.query.get(category_id)
        
        if not category:
            raise NotFoundError(f"Category with ID {category_id} not found")
        
        # Check if category has products
        product_count = category.products.count()
        
        if product_count > 0 and not force:
            raise ValidationError(
                f"Cannot delete category with {product_count} products. "
                "Use force=true to delete category and remove category assignment from products."
            )
        
        if force and product_count > 0:
            # Remove category assignment from all products
            for product in category.products:
                product.category_id = None
        
        db.session.delete(category)
        db.session.commit()
        
        message = "Category deleted successfully"
        if force and product_count > 0:
            message += f" and removed category assignment from {product_count} products"
        
        return success_response(None, message)
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except ValidationError as e:
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        db.session.rollback()
        return error_response("INTERNAL_ERROR", f"Failed to delete category: {str(e)}")

@categories_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def get_category_products(category_id):
    """Get all products in a specific category.
    
    Query Parameters:
    - page: Page number for pagination (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - sort_by: Sort field (name, price, created_at)
    - sort_order: Sort order (asc, desc)
    """
    try:
        category = Category.query.get(category_id)
        
        if not category:
            raise NotFoundError(f"Category with ID {category_id} not found")
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc')
        
        # Build query
        query = category.products
        
        # Apply sorting
        if sort_by in ['name', 'price', 'created_at', 'stock_quantity']:
            # Product is already imported at the top
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
        products_data = [product.to_dict(include_category=False) for product in products]
        
        response_data = {
            'category': category.to_dict(),
            'products': products_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
        
        return success_response(response_data, "Category products retrieved successfully")
        
    except NotFoundError as e:
        return error_response("NOT_FOUND", str(e), status_code=404)
    except Exception as e:
        return error_response("INTERNAL_ERROR", f"Failed to retrieve category products: {str(e)}")