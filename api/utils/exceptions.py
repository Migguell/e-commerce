"""Custom exception classes for the e-commerce backend API."""

class APIException(Exception):
    """Base exception class for API-related errors."""
    
    def __init__(self, message, status_code=500, error_code=None, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

class ValidationError(APIException):
    """Exception raised for input validation errors."""
    
    def __init__(self, message, field=None, details=None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details or {}
        )
        self.field = field
        if field:
            self.details['field'] = field

class NotFoundError(APIException):
    """Exception raised when a requested resource is not found."""
    
    def __init__(self, resource="Resource", resource_id=None, details=None):
        if resource_id:
            message = f"{resource} with ID {resource_id} not found"
        else:
            message = f"{resource} not found"
        
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details=details or {}
        )
        self.resource = resource
        self.resource_id = resource_id

class BusinessLogicError(APIException):
    """Exception raised for business logic violations."""
    
    def __init__(self, message, error_code="BUSINESS_LOGIC_ERROR", details=None):
        super().__init__(
            message=message,
            status_code=400,
            error_code=error_code,
            details=details or {}
        )

class ConflictError(APIException):
    """Exception raised for resource conflicts."""
    
    def __init__(self, message, resource=None, details=None):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT",
            details=details or {}
        )
        self.resource = resource

class InsufficientStockError(BusinessLogicError):
    """Exception raised when there's insufficient stock for a product."""
    
    def __init__(self, product_id, requested_quantity, available_quantity):
        message = f"Insufficient stock for product {product_id}. Requested: {requested_quantity}, Available: {available_quantity}"
        details = {
            'product_id': product_id,
            'requested_quantity': requested_quantity,
            'available_quantity': available_quantity
        }
        super().__init__(
            message=message,
            error_code="INSUFFICIENT_STOCK",
            details=details
        )
        self.product_id = product_id
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity

class DuplicateResourceError(ConflictError):
    """Exception raised when trying to create a duplicate resource."""
    
    def __init__(self, resource, field, value, details=None):
        message = f"{resource} with {field} '{value}' already exists"
        conflict_details = {
            'field': field,
            'value': value
        }
        if details:
            conflict_details.update(details)
        
        super().__init__(
            message=message,
            resource=resource,
            details=conflict_details
        )
        self.field = field
        self.value = value

class InvalidOperationError(BusinessLogicError):
    """Exception raised for invalid operations."""
    
    def __init__(self, operation, reason, details=None):
        message = f"Invalid operation '{operation}': {reason}"
        super().__init__(
            message=message,
            error_code="INVALID_OPERATION",
            details=details or {}
        )
        self.operation = operation
        self.reason = reason

class DatabaseError(APIException):
    """Exception raised for database-related errors."""
    
    def __init__(self, message, operation=None, details=None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            details=details or {}
        )
        self.operation = operation
        if operation:
            self.details['operation'] = operation

class ExternalServiceError(APIException):
    """Exception raised for external service errors."""
    
    def __init__(self, service, message, status_code=503, details=None):
        full_message = f"External service '{service}' error: {message}"
        super().__init__(
            message=full_message,
            status_code=status_code,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details or {}
        )
        self.service = service
        self.details['service'] = service

class RateLimitError(APIException):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, limit, window, retry_after=None, details=None):
        message = f"Rate limit exceeded: {limit} requests per {window}"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        
        rate_details = {
            'limit': limit,
            'window': window
        }
        if retry_after:
            rate_details['retry_after'] = retry_after
        if details:
            rate_details.update(details)
        
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details=rate_details
        )
        self.limit = limit
        self.window = window
        self.retry_after = retry_after

class AuthenticationError(APIException):
    """Exception raised for authentication failures."""
    
    def __init__(self, message="Authentication failed", details=None):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
            details=details or {}
        )

class AuthorizationError(APIException):
    """Exception raised for authorization failures."""
    
    def __init__(self, message="Access forbidden", resource=None, action=None, details=None):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
            details=details or {}
        )
        self.resource = resource
        self.action = action
        if resource:
            self.details['resource'] = resource
        if action:
            self.details['action'] = action