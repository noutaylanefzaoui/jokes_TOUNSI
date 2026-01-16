from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import abort


def role_required(*allowed_roles):
    """
    Decorator to check if user has required role.
    
    Usage:
        @role_required("admin")
        @role_required("admin", "contributor")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT exists and is valid
            verify_jwt_in_request()
            
            # Get user's role from JWT claims
            claims = get_jwt()
            user_role = claims.get("role", "user")
            
            # Check if role is allowed
            if user_role not in allowed_roles:
                abort(403, description=f"Admin access required. You have role: {user_role}")
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator