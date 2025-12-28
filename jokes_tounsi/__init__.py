from flask import Flask, jsonify
from .config import DevelopmentConfig
from .extensions import db, api, jwt, oauth

# NEW: import the meta blueprint
from .resources.meta import blp as MetaBlueprint


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    # Register blueprints with Flask-Smorest
    api.register_blueprint(MetaBlueprint, url_prefix="/api/v1")

    # Simple health route (plain Flask, outside Flask-Smorest)
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "jokesTOUNSI"})

    return app
