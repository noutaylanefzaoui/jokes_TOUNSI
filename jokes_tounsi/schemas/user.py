from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.user import User


class UserRegisterSchema(Schema):
    """Schema for user registration input."""
    
    email = fields.Email(required=True, validate=validate.Length(min=1, max=120))
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=255),
        load_only=True  # Password never returned in responses
    )
    display_name = fields.String(required=True, validate=validate.Length(min=1, max=120))


class UserLoginSchema(Schema):
    """Schema for login input."""
    
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class UserSchema(Schema):
    """Schema for user output (no password)."""
    
    id = fields.Integer(dump_only=True)  # dump_only = only in responses, not input
    email = fields.Email()
    display_name = fields.String()
    role = fields.String()
    created_at = fields.DateTime(dump_only=True)


class UserRoleSchema(Schema):
    """Schema for changing user role (admin only)."""
    
    email = fields.Email(required=True)
    role = fields.String(
        required=True,
        validate=validate.OneOf(["user", "contributor", "admin"])
    )