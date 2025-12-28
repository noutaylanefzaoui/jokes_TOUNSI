from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db, oauth
from ..models import User
from ..schemas import UserRegisterSchema, UserLoginSchema, UserSchema
from flask import url_for, redirect, current_app



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

@blp.route("/auth/google/login")
class GoogleLogin(MethodView):
    def get(self):
        """
        Redirect the user to Google's OAuth2 consent screen.
        """
        redirect_uri = url_for(
            "auth.GoogleCallback",  # blueprint-name.ClassName
            _external=True,
        )
        return oauth.google.authorize_redirect(redirect_uri)
    
@blp.route("/auth/google/callback")
class GoogleCallback(MethodView):
    def get(self):
        """
        Handle the OAuth2 callback from Google:
        - Get user info from Google via Authlib
        - Find or create a local User
        - Issue a JWT access token
        """
        try:
            token = oauth.google.authorize_access_token()
            user_info = token.get("userinfo")
            if not user_info:
                # Fallback: some setups put data in id_token; but for now userinfo is enough
                abort(400, message="Could not get user info from Google.")
        except Exception as e:
            print("GOOGLE OAUTH ERROR:", repr(e))
            abort(400, message="Google OAuth error.")

        google_id = user_info.get("sub")
        email = user_info.get("email")
        name = user_info.get("name") or (email.split("@")[0] if email else None)

        if not email:
            abort(400, message="Google account has no email.")

        # Find existing user by google_id or email
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            user = User.query.filter_by(email=email).first()

        if not user:
            user = User(
                email=email,
                display_name=name,
                role="user",
                google_id=google_id,
                password_hash="",  # no local password for Google-only accounts
            )
            db.session.add(user)
        else:
            if not user.google_id:
                user.google_id = google_id

        db.session.commit()

        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
        )

        return {"access_token": access_token}, 200


        db.session.commit()

        # Issue JWT for this user
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
        )

        # You can either redirect to a front-end with token as query param,
        # or just return JSON for now.
        return {"access_token": access_token}, 200
