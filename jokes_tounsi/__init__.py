from flask import Flask, jsonify
from .config import DevelopmentConfig
from .extensions import db, api, jwt, oauth
from .resources.meta import blp as MetaBlueprint
from .resources.jokes import blp as JokesBlueprint  # if you already added this
from .resources.auth import blp as AuthBlueprint
from .models import User, Joke

from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended import verify_jwt_in_request
from werkzeug.exceptions import HTTPException
from .utils.logging_config import configure_logging

def create_app(config_class=DevelopmentConfig):
    configure_logging()
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"message": "Missing or invalid Authorization header"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"message": "Invalid token DEBUG", "reason": reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    # register blueprints as before
    api.register_blueprint(MetaBlueprint, url_prefix="/api/v1")
    api.register_blueprint(JokesBlueprint, url_prefix="/api/v1")
    api.register_blueprint(AuthBlueprint, url_prefix="/api/v1")
        # error handlers
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        # All HTTP errors (404, 405, etc.) as JSON
        response = {
            "code": e.code,
            "message": e.description,
            "status": e.name,
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        # Unexpected errors as generic 500 JSON
        response = {
            "code": 500,
            "message": "Internal server error",
            "status": "InternalServerError",
        }
        return jsonify(response), 500

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "jokesTOUNSI"})

    with app.app_context():
        db.create_all()

    return app
