import logging
from flask import request
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.exceptions import Conflict

from ..extensions import db
from ..models import User
from ..schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserSchema,
    UserRoleSchema
)

logger = logging.getLogger(__name__)

blp = Blueprint(
    "auth",
    __name__,
    description="Authentication and authorization"
)


@blp.route("/register", methods=["POST"])
@blp.arguments(UserRegisterSchema, location="json")
@blp.response(201, UserSchema)
def register(args):
    """Register a new user."""
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=args["email"]).first()
    if existing_user:
        abort(409, message=f"User with email {args['email']} already exists")
    
    # Create new user
    user = User(
        email=args["email"],
        display_name=args["display_name"],
        role="user"  # Default role
    )
    user.set_password(args["password"])
    
    # Save to database
    try:
        db.session.add(user)
        db.session.commit()
        logger.info(f"User registered: {user.email}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration failed: {str(e)}")
        abort(500, message="Error registering user")
    
    return user, 201



@blp.route("/login", methods=["POST"])
@blp.arguments(UserLoginSchema, location="json")
def login(args):
    """Login user with email and password."""
    
    # Find user by email
    user = User.query.filter_by(email=args["email"]).first()
    
    # Check credentials
    if not user or not user.check_password(args["password"]):
        logger.warning(f"Failed login attempt for {args['email']}")
        abort(401, message="Invalid email or password")
    
    # Create JWT token with role claim
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user": user.to_dict()
    }


@blp.route("/users/me", methods=["GET"])
@jwt_required()
@blp.response(200, UserSchema)
def get_current_user():
    """Get current authenticated user's profile."""
    
    user_id = get_jwt_identity()          # identity is a str
    user = User.query.get(int(user_id))   # convert to int for DB lookup
    
    if not user:
        abort(404, message="User not found")
    
    # IMPORTANT: return the model instance, not .to_dict()
    return user

@blp.route("/users/role", methods=["PUT"])
@jwt_required()
@blp.arguments(UserRoleSchema, location="json")
@blp.response(200, UserSchema)
def change_user_role(args):
    """
    Change a user's role (admin only).
    Body: { "email": "...", "role": "user|contributor|admin" }
    """
    claims = get_jwt()
    current_role = claims.get("role")
    if current_role != "admin":
        abort(403, message="You do not have permission to change roles")

    user = User.query.filter_by(email=args["email"]).first()
    if not user:
        abort(404, message="User not found")

    user.role = args["role"]
    try:
        db.session.commit()
        logger.info(f"Role of {user.email} changed to {user.role}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to change role: {str(e)}")
        abort(500, message="Error changing user role")

    # IMPORTANT: return the model, not .to_dict()
    return user


@blp.route("/debug-users", methods=["GET"])
def debug_users():
    """Temporary: list all users for debugging."""
    users = User.query.all()
    return [u.to_dict() for u in users], 200
