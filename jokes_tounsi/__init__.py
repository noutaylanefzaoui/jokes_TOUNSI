from flask import Flask, jsonify
from .config import DevelopmentConfig
from .extensions import db, api, jwt, oauth
from .resources.meta import blp as MetaBlueprint
from .resources.jokes import blp as JokesBlueprint  # if you already added this
from .models import User, Joke



def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    api.register_blueprint(MetaBlueprint, url_prefix="/api/v1")
    api.register_blueprint(JokesBlueprint, url_prefix="/api/v1")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "jokesTOUNSI"})

    # Create tables on startup (simple dev approach)
    with app.app_context():
        db.create_all()

    return app
