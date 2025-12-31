from flask.views import MethodView
from flask_smorest import Blueprint
from ..utils.constants import (
    AGE_GROUPS,
    ERAS,
    REGIONS,
    ACCEPTABILITY_LEVELS,
    DELIVERY_TYPES,
)


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

@blp.route("/meta/classification")
class ClassificationMeta(MethodView):
    @blp.response(200)
    def get(self):
        """
        Return allowed classification values for jokes.
        """
        return {
            "age_groups": AGE_GROUPS,
            "eras": ERAS,
            "regions": REGIONS,
            "acceptability_levels": ACCEPTABILITY_LEVELS,
            "delivery_types": DELIVERY_TYPES,
        }
