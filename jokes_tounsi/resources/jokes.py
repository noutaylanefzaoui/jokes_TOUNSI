from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from ..extensions import db
from ..models import Joke
from ..schemas import JokeSchema, JokeCreateSchema, JokeListQueryArgs

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

@blp.route("/jokes/<int:joke_id>")
class JokeDetail(MethodView):
    @blp.response(200, JokeSchema)
    def get(self, joke_id):
        """
        Get a single joke by its ID.
        """
        joke = Joke.query.get(joke_id)
        if not joke:
            abort(404, message="Joke not found.")
        return joke
