import os
import pytest
from dotenv import load_dotenv
from jokes_tounsi import create_app
from jokes_tounsi.extensions import db
from jokes_tounsi.config import TestingConfig


@pytest.fixture
def app():
    """Create app with testing config."""
    # Load .env
    load_dotenv()
    
    # Create app with testing config
    app = create_app(TestingConfig)
    
    # Create tables in memory database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner."""
    return app.test_cli_runner()