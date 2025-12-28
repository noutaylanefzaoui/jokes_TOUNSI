from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import User
from ..schemas import UserRegisterSchema, UserLoginSchema, UserSchema


blp = Blueprint(
    "auth",
    "auth",
    description="User registration, login and current user info",
)


@blp.route("/auth/register")
class Register(MethodView):

    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        # Check if email already exists
        if User.query.filter_by(email=user_data["email"]).first():
            abort(409, message="Email is already registered.")

        user = User(
            email=user_data["email"],
            display_name=user_data["display_name"],
            role="user",
        )
        user.set_password(user_data["password"])  # secure hash

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error creating user.")

        return user


@blp.route("/auth/login")
class Login(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        user = User.query.filter_by(email=login_data["email"]).first()

        if not user or not user.check_password(login_data["password"]):
            abort(401, message="Invalid email or password.")

        # identity will be user.id, we can add role as extra claim later
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=str(user.id),  # must be string
            additional_claims=additional_claims,
        )

        return {"access_token": access_token}, 200

@blp.route("/users/me")
class Me(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        user_id_str = get_jwt_identity()  # identity is a string
        user_id = int(user_id_str)        # convert to int for DB lookup

        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        return user
    
@blp.route("/auth/test-token")
class TestToken(MethodView):

    @jwt_required()
    def get(self):
        from flask_jwt_extended import get_jwt
        return {"jwt": get_jwt()}, 200
