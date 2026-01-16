from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate

db = SQLAlchemy()
api = Api()
jwt = JWTManager()
oauth = OAuth()
migrate = Migrate()
