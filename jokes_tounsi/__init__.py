import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .config import DevelopmentConfig
from .extensions import db, api, jwt, oauth, migrate
from .resources.meta import blp as MetaBlueprint
from .resources.jokes import blp as JokesBlueprint
from .resources.auth import blp as AuthBlueprint
from .utils.logging_config import configure_logging

def create_app(config_class=DevelopmentConfig):
    configure_logging()  

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


    api.register_blueprint(MetaBlueprint, url_prefix="/api/v1")
    api.register_blueprint(JokesBlueprint, url_prefix="/api/v1")
    api.register_blueprint(AuthBlueprint, url_prefix="/api/v1")

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = dict(code=e.code, message=e.description, status=e.name)
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        response = dict(code=500, message="Internal server error", status="InternalServerError")
        return jsonify(response), 500

    @app.route("/health")
    def health():
        return jsonify(status="ok", app="jokesTOUNSI")


    return app
