from jokes_tounsi import create_app
from jokes_tounsi.extensions import db
from jokes_tounsi.models import User, Joke

app = create_app()

with app.app_context():
    joke = Joke.query.get(1)
    if joke:
        print("Joke 1 author_id:", joke.author_id)
    else:
        print("Joke 1 not found")

    for user in User.query.all():
        print("User:", user.id, user.email, "role:", user.role)
