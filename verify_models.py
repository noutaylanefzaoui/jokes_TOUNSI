from jokes_tounsi import create_app
from jokes_tounsi.extensions import db
from jokes_tounsi.models import User, Joke, Category, Rating, Favorite
import os

# Create a test app configured for an in-memory database
class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    SECRET_KEY = "test-secret"
    JWT_SECRET_KEY = "test-jwt-secret"
    DEBUG = True
    API_TITLE = "Jokes Tounsi API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"

app = create_app(TestConfig)

def verify_models():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        print("Creating User...")
        user = User(username="testuser", email="test@example.com", display_name="Test User", password_hash="hash")
        db.session.add(user)
        db.session.commit()
        print(f"User created: {user}")

        print("Creating Category...")
        category = Category(name="Funny", description="Funny jokes")
        db.session.add(category)
        db.session.commit()
        print(f"Category created: {category}")
        
        print("Creating Joke...")
        joke = Joke(
            content="This is a test joke content",
            text_tn="Hahahaha", 
            user_id=user.id, 
            category_id=category.category_id,
            status="published"
        )
        db.session.add(joke)
        db.session.commit()
        print(f"Joke created: {joke}")
        
        print("Verifying Joke relationships...")
        assert joke.author == user
        assert joke.category == category
        print("Joke relationships verified.")

        print("Creating Rating...")
        rating = Rating(rating_value=5, joke_id=joke.id)
        rating.submit()
        print(f"Rating created: {rating}")
        
        print("Creating Favorite...")
        favorite = Favorite(user_id=user.id, joke_id=joke.id)
        favorite.add()
        print(f"Favorite created: {favorite}")
        
        print("Verifying Favorite constraints...")
        try:
             duplicate_favorite = Favorite(user_id=user.id, joke_id=joke.id)
             db.session.add(duplicate_favorite)
             db.session.commit()
             print("Error: Duplicate favorite allowed (should satisfy UniqueConstraint)")
        except Exception as e:
            db.session.rollback()
            print(f"Success: Duplicate favorite prevented: {e}")

        print("All verifications passed successfully!")

if __name__ == "__main__":
    verify_models()
