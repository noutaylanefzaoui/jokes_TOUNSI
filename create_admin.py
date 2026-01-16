from jokes_tounsi import create_app
from jokes_tounsi.extensions import db
from jokes_tounsi.models import User

app = create_app()

with app.app_context():
    # Make sure tables exist
    db.create_all()

    email = "admin@example.com"
    password = "admin123"

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            email=email,
            display_name="Admin",
            role="admin",
        )
        user.set_password(password)
        db.session.add(user)
        print("Admin user created")
    else:
        user.role = "admin"
        user.set_password(password)
        print("Admin user updated")

    db.session.commit()
    print("Admin ready:", user.email, user.role)
