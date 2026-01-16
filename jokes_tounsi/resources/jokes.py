import logging
from flask import request
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import User, Joke
from ..schemas import (
    JokeCreateSchema,
    JokeUpdateSchema,
    JokeSchema,
    JokeListQueryArgsSchema,
    JokeListResponseSchema
)
from ..security import role_required

logger = logging.getLogger(__name__)

blp = Blueprint(
    "jokes",
    __name__,
    description="Joke CRUD operations, search, and filtering"
)



@blp.route("/jokes", methods=["GET"])
@blp.arguments(JokeListQueryArgsSchema, location="query")
@blp.response(200, JokeListResponseSchema)
def list_jokes(args):
    """
    List all jokes with pagination and filtering.
    
    Query parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - era: Filter by era
    - region: Filter by region
    - age_group: Filter by age group
    - acceptability: Filter by acceptability
    - delivery_type: Filter by delivery type
    - q: Search in joke text
    """
    
    # Start with base query (only published jokes)
    query = Joke.query.filter_by(is_published=True)
    
    # Apply filters if provided
    if args.get("era"):
        query = query.filter_by(era=args["era"])
    
    if args.get("region"):
        query = query.filter_by(region=args["region"])
    
    if args.get("age_group"):
        query = query.filter_by(age_group=args["age_group"])
    
    if args.get("acceptability"):
        query = query.filter_by(acceptability=args["acceptability"])
    
    if args.get("delivery_type"):
        query = query.filter_by(delivery_type=args["delivery_type"])
    
    # Search in text if provided
    if args.get("q"):
        search_term = f"%{args['q']}%"
        query = query.filter(
            Joke.text_tn.ilike(search_term) |
            Joke.text_fr.ilike(search_term) |
            Joke.text_en.ilike(search_term)
        )
    
    # Pagination
    page = args["page"]
    per_page = args["per_page"]
    pagination = query.order_by(Joke.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
    "page": page,
    "per_page": per_page,
    "total": pagination.total,
    "items": pagination.items
}



@blp.route("/jokes", methods=["POST"])
@jwt_required()
@blp.arguments(JokeCreateSchema, location="json")
@blp.response(201, JokeSchema)
def create_joke(args):  
    """Create a new joke (contributor or admin only)."""
    
    # Get current user
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    # Check permission
    if user.role not in ["contributor", "admin"]:
        abort(403, message="Only contributors and admins can create jokes")
    
    # Create joke
    joke = Joke(
        text_tn=args["text_tn"],
        text_fr=args.get("text_fr"),
        text_en=args.get("text_en"),
        age_group=args.get("age_group"),
        era=args.get("era"),
        region=args.get("region"),
        acceptability=args.get("acceptability"),
        delivery_type=args.get("delivery_type"),
        tone=args.get("tone"),
        rhythm=args.get("rhythm"),
        is_published=args.get("is_published", False),
        author_id=user.id
    )
    
    # Save to database
    try:
        db.session.add(joke)
        db.session.commit()
        logger.info(f"Joke created by {user.email}: {joke.id}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating joke: {str(e)}")
        abort(500, message="Error creating joke")
    
    return joke, 201



@blp.route("/jokes/<int:joke_id>", methods=["GET"])
@blp.response(200, JokeSchema)
def get_joke(joke_id):
    """Get a single joke by ID."""
    
    joke = Joke.query.get(joke_id)
    if not joke:
        abort(404, message=f"Joke {joke_id} not found")
    
    return joke



@blp.route("/jokes/<int:joke_id>", methods=["PATCH"])
@jwt_required()
@blp.arguments(JokeUpdateSchema, location="json")
@blp.response(200, JokeSchema)
def update_joke(args, joke_id):
    """Update a joke (contributor/admin only)."""
    
    # Get joke
    joke = Joke.query.get(joke_id)
    if not joke:
        abort(404, message=f"Joke {joke_id} not found")
    
    # Get current user
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    # Check permission (author or admin)
    if joke.author_id != user.id and user.role != "admin":
        abort(403, message="You can only edit your own jokes")
    
    # Update fields if provided
    if args.get("text_tn"):
        joke.text_tn = args["text_tn"]
    if args.get("text_fr"):
        joke.text_fr = args["text_fr"]
    if args.get("text_en"):
        joke.text_en = args["text_en"]
    if args.get("age_group"):
        joke.age_group = args["age_group"]
    if args.get("era"):
        joke.era = args["era"]
    if args.get("region"):
        joke.region = args["region"]
    if args.get("acceptability"):
        joke.acceptability = args["acceptability"]
    if args.get("delivery_type"):
        joke.delivery_type = args["delivery_type"]
    if args.get("tone"):
        joke.tone = args["tone"]
    if args.get("rhythm"):
        joke.rhythm = args["rhythm"]
    if args.get("is_published") is not None:
        joke.is_published = args["is_published"]
    
    # Save
    try:
        db.session.commit()
        logger.info(f"Joke {joke_id} updated by {user.email}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating joke: {str(e)}")
        abort(500, message="Error updating joke")
    
    return joke  # not joke.to_dict()



@blp.route("/jokes/<int:joke_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_joke(joke_id):
    """Delete a joke (admin only)."""
    
    joke = Joke.query.get(joke_id)
    if not joke:
        abort(404, message=f"Joke {joke_id} not found")
    
    # Get current user for logging
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    # Delete
    try:
        db.session.delete(joke)
        db.session.commit()
        logger.info(f"Joke {joke_id} deleted by {user.email}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting joke: {str(e)}")
        abort(500, message="Error deleting joke")
    
    return "", 204