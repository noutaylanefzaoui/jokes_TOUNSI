from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from ..extensions import db
from ..models import Joke
from ..schemas import JokeSchema, JokeCreateSchema

blp = Blueprint(
    "jokes",
    "jokes",
    description="Basic operations on jokes (no auth yet)",
)


@blp.route("/jokes")
class JokesList(MethodView):
    @blp.response(200, JokeSchema(many=True))
    def get(self):
        """
        Return all jokes for now.
        Later we will add pagination and filtering.
        """
        jokes = Joke.query.all()
        return jokes

    @blp.arguments(JokeCreateSchema)
    @blp.response(201, JokeSchema)
    def post(self, joke_data):
        """
        Create a new joke.
        For now there is no authentication; later we'll restrict this.
        """
        joke = Joke(**joke_data)
        try:
            db.session.add(joke)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error saving joke to the database.")

        return joke
