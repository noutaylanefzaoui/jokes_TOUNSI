from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..extensions import db
from ..models import Joke
from ..schemas import JokeSchema, JokeCreateSchema, JokeListQueryArgs
from ..security import role_required



blp = Blueprint(
    "jokes",
    "jokes",
    description="Basic operations on jokes (no auth yet)",
)


@blp.route("/jokes")
class JokesList(MethodView):

    @blp.arguments(JokeListQueryArgs, location="query")
    @blp.response(200)
    def get(self, query_args):
        """
        List jokes with basic filtering and pagination.
        """
        page = query_args["page"]
        per_page = query_args["per_page"]

        query = Joke.query

        # Apply filters only if provided
        if query_args.get("age_group"):
            query = query.filter(Joke.age_group == query_args["age_group"])

        if query_args.get("era"):
            query = query.filter(Joke.era == query_args["era"])

        if query_args.get("region"):
            query = query.filter(Joke.region == query_args["region"])

        if query_args.get("acceptability"):
            query = query.filter(Joke.acceptability == query_args["acceptability"])

        if query_args.get("delivery_type"):
            query = query.filter(Joke.delivery_type == query_args["delivery_type"])

        if query_args.get("q"):
            like_value = f"%{query_args['q']}%"
            query = query.filter(Joke.text_tn.ilike(like_value))

        # Paginate
        pagination = query.order_by(Joke.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        items = JokeSchema(many=True).dump(pagination.items)

        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "items": items,
        }
    @role_required("contributor", "admin")
    @blp.arguments(JokeCreateSchema)
    @blp.response(201, JokeSchema)
    def post(self, joke_data):
        """
        Create a new joke.
        Only contributors and admins can create jokes.
        The author_id is set from the current user.
        """
        user_id_str = get_jwt_identity()
        author_id = int(user_id_str)

        joke = Joke(**joke_data, author_id=author_id)
        try:
            db.session.add(joke)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error saving joke to the database.")

        return joke

@blp.route("/jokes/<int:joke_id>")
class JokeDetail(MethodView):
    @blp.response(200, JokeSchema)
    def get(self, joke_id):
        joke = Joke.query.get(joke_id)
        if not joke:
            abort(404, message="Joke not found.")
        return joke

    @role_required("contributor", "admin")
    @blp.arguments(JokeCreateSchema(partial=True))
    @blp.response(200, JokeSchema)
    def patch(self, update_data, joke_id):
        """
        Update a joke.
        Contributors can update only their own jokes.
        Admins can update any joke.
        """
        joke = Joke.query.get(joke_id)
        if not joke:
            abort(404, message="Joke not found.")

        user_id = int(get_jwt_identity())
        claims = get_jwt()
        role = claims.get("role")

        if role != "admin" and joke.author_id != user_id:
            abort(403, message="You can only edit your own jokes.")

        for key, value in update_data.items():
            setattr(joke, key, value)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error updating joke.")

        return joke

    @role_required("admin")
    def delete(self, joke_id):
        """
        Delete a joke.
        Only admins are allowed to delete jokes.
        """
        joke = Joke.query.get(joke_id)
        if not joke:
            abort(404, message="Joke not found.")

        try:
            db.session.delete(joke)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error deleting joke.")

        return {"message": "Joke deleted successfully."}
