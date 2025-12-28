from functools import wraps
from flask_smorest import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*allowed_roles):
    """
    Decorator that requires the user to have one of the given roles.
    Example: @role_required("admin", "contributor")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Ensure a valid JWT is present
            verify_jwt_in_request()

            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed_roles:
                abort(403, message="You do not have permission to perform this action.")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
