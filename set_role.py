from jokes_tounsi import create_app
from jokes_tounsi.extensions import db
from jokes_tounsi.models import User

app = create_app()

with app.app_context():
    # change this email to your user email
    email = "noutayla@example.com"

    user = User.query.filter_by(email=email).first()
    if not user:
        print("User not found")
    else:
        print("Old role:", user.role)
        user.role = "contributor"   # or "admin"
        db.session.commit()
        print("New role:", user.role)
