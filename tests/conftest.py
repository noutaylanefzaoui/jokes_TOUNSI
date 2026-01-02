import os
import pytest

from jokes_tounsi import create_app, db


@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing"
    # use a separate SQLite DB for tests
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
