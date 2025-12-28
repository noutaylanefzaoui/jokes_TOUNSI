from flask import Flask, jsonify
from .config import DevelopmentConfig
from .extensions import db, api, jwt, oauth


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    # Simple health check route (no blueprints yet)
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "jokesTOUNSI"})

    return app
