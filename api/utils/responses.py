"""Standardized API response helpers."""

from flask import jsonify
from datetime import datetime

__all__ = [
    'success_response',
    'error_response',
    'validation_error_response',
    'not_found_response',
    'conflict_response',
    'server_error_response',
    'paginated_response',
    'created_response',
    'no_content_response',
    'bad_request_response',
    'unauthorized_response',
    'forbidden_response'
]

def success_response(data=None, message="Success", status_code=200, meta=None):
    """Create a standardized success response.
    
    Args:
        data: Response data (can be dict, list, or any JSON-serializable object)
        message (str): Success message
        status_code (int): HTTP status code
        meta (dict): Additional metadata (pagination, etc.)
    
    Returns:
        Flask Response: JSON response with standardized format
    """
    response_data = {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if meta:
        response_data["meta"] = meta
    
    return jsonify(response_data), status_code

def error_response(message="An error occurred", status_code=400, error_code=None, details=None):
    """Create a standardized error response.
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        error_code (str): Application-specific error code
        details (dict): Additional error details
    
    Returns:
        Flask Response: JSON response with standardized error format
    """
    response_data = {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if error_code:
        response_data["error_code"] = error_code
    
    if details:
        response_data["details"] = details
    
    return jsonify(response_data), status_code

def validation_error_response(message="Validation failed", errors=None):
    """Create a validation error response.
    
    Args:
        message (str): Main error message
        errors (dict or list): Specific validation errors
    
    Returns:
        Flask Response: JSON response for validation errors
    """
    details = {}
    if errors:
        details["validation_errors"] = errors
    
    return error_response(
        message=message,
        status_code=422,
        error_code="VALIDATION_ERROR",
        details=details
    )

def not_found_response(resource="Resource", resource_id=None):
    """Create a not found error response.
    
    Args:
        resource (str): Name of the resource that wasn't found
        resource_id: ID of the resource that wasn't found
    
    Returns:
        Flask Response: JSON response for not found errors
    """
    if resource_id:
        message = f"{resource} with ID {resource_id} not found"
    else:
        message = f"{resource} not found"
    
    return error_response(
        message=message,
        status_code=404,
        error_code="NOT_FOUND"
    )

def conflict_response(message="Resource conflict", details=None):
    """Create a conflict error response.
    
    Args:
        message (str): Conflict error message
        details (dict): Additional conflict details
    
    Returns:
        Flask Response: JSON response for conflict errors
    """
    return error_response(
        message=message,
        status_code=409,
        error_code="CONFLICT",
        details=details
    )

def server_error_response(message="Internal server error"):
    """Create a server error response.
    
    Args:
        message (str): Server error message
    
    Returns:
        Flask Response: JSON response for server errors
    """
    return error_response(
        message=message,
        status_code=500,
        error_code="INTERNAL_ERROR"
    )

def paginated_response(items, page, per_page, total_items, message="Success"):
    """Create a paginated response.
    
    Args:
        items (list): List of items for current page
        page (int): Current page number
        per_page (int): Items per page
        total_items (int): Total number of items
        message (str): Success message
    
    Returns:
        Flask Response: JSON response with pagination metadata
    """
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
    
    meta = {
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None
        }
    }
    
    return success_response(
        data=items,
        message=message,
        meta=meta
    )

def created_response(data=None, message="Resource created successfully", location=None):
    """Create a resource created response.
    
    Args:
        data: Created resource data
        message (str): Success message
        location (str): Location header value (resource URL)
    
    Returns:
        Flask Response: JSON response for created resources
    """
    response = success_response(
        data=data,
        message=message,
        status_code=201
    )
    
    if location:
        response[0].headers['Location'] = location
    
    return response

def no_content_response():
    """Create a no content response.
    
    Returns:
        Flask Response: Empty response with 204 status
    """
    return '', 204

def bad_request_response(message="Bad request", details=None):
    """Create a bad request error response.
    
    Args:
        message (str): Error message
        details (dict): Additional error details
    
    Returns:
        Flask Response: JSON response for bad request errors
    """
    return error_response(
        message=message,
        status_code=400,
        error_code="BAD_REQUEST",
        details=details
    )

def unauthorized_response(message="Unauthorized access"):
    """Create an unauthorized error response.
    
    Args:
        message (str): Error message
    
    Returns:
        Flask Response: JSON response for unauthorized errors
    """
    return error_response(
        message=message,
        status_code=401,
        error_code="UNAUTHORIZED"
    )

def forbidden_response(message="Access forbidden"):
    """Create a forbidden error response.
    
    Args:
        message (str): Error message
    
    Returns:
        Flask Response: JSON response for forbidden errors
    """
    return error_response(
        message=message,
        status_code=403,
        error_code="FORBIDDEN"
    )