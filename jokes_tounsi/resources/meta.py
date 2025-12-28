from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    "meta",
    "meta",
    description="Meta information about the jokesTOUNSI API",
)

@blp.route("/meta/ping")
class MetaPing(MethodView):
    @blp.response(200)
    def get(self):
        """
        Simple endpoint to test Flask-Smorest and Swagger.
        """
        return {"message": "jokesTOUNSI API is alive"}
