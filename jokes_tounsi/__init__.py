import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .config import DevelopmentConfig
from .extensions import db, api, jwt, oauth
from .resources.meta import blp as MetaBlueprint
from .resources.jokes import blp as JokesBlueprint
from .resources.auth import blp as AuthBlueprint
from .utils.logging_config import configure_logging

from flask_migrate import Migrate

migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    configure_logging()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    # Google OAuth registration
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"message": "Missing or invalid Authorization header"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"message": "Invalid token DEBUG", "reason": reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    # Register blueprints
    api.register_blueprint(MetaBlueprint, url_prefix="/api/v1")
    api.register_blueprint(JokesBlueprint, url_prefix="/api/v1")
    api.register_blueprint(AuthBlueprint, url_prefix="/api/v1")

    # Error handlers
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "code": e.code,
            "message": e.description,
            "status": e.name,
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        response = {
            "code": 500,
            "message": "Internal server error",
            "status": "InternalServerError",
        }
        return jsonify(response), 500

    # Health check
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "jokesTOUNSI"})

    # IMPORTANT: no db.drop_all() or db.create_all() here.
    # Database schema is managed via Flask-Migrate (flask db upgrade).

    return app
