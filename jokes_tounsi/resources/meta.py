from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Joke, User


blp = Blueprint(
    "meta",
    __name__,
    url_prefix="/api/v1/meta",
    description="API metadata and health endpoints"
)


@blp.route("/ping", methods=["GET"])
def ping():
    """API health check endpoint."""
    return {"status": "pong", "message": "API is healthy"}


@blp.route("/classification", methods=["GET"])
def get_classification():
    """Get all classification values used in the system."""
    return {
        "eras": ["Pre-2011", "Post-2011"],
        "regions": ["Tunis", "Sfax", "Ariana", "Ben Arous", "Sousse", "Kairouan"],
        "age_groups": ["Kids", "Teens", "Adults", "Elders"],
        "acceptability_levels": ["Safe", "Sensitive", "Taboo"],
        "delivery_types": ["Radio", "TV", "Stand-up", "Book", "Oral"],
        "tones": ["Sarcastic", "Funny", "Dark", "Subtle", "Witty"],
        "rhythms": ["Fast", "Slow", "Medium"]
    }