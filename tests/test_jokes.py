from jokes_tounsi.models import User
from jokes_tounsi.extensions import db


def create_contributor(app):
    with app.app_context():
        user = User(
            email="contrib@example.com",
            display_name="Contributor",
            role="contributor",
        )
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()
        return user.email


def login_contributor(client, email):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "secret123"},
    )


def test_create_and_list_joke(app, client):
    email = create_contributor(app)
    login_resp = login_contributor(client, email)
    token = login_resp.get_json()["access_token"]

    joke_body = {
        "text_tn": "مرة توانسة في الكار...",
        "text_fr": "Blague tunisienne.",
        "text_en": "Tunisian joke.",
        "age_group": "adults",
        "era": "post-2020",
        "region": "Tunis",
        "acceptability": "safe",
        "delivery_type": "radio",
        "tone": "sarcastic",
        "rhythm": "fast",
        "is_published": True,
    }

    create_resp = client.post(
        "/api/v1/jokes",
        json=joke_body,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_resp.status_code == 201
    joke = create_resp.get_json()
    assert joke["region"] ==    "Tunis"

    list_resp = client.get("/api/v1/jokes?region=Tunis")
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert any(item["id"] == joke["id"] for item in data["items"])
