import json


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/api/v1/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "display_name": "Test User"
        }
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert "password" not in data  # Password should never be returned


def test_register_duplicate_email(client):
    """Test registration with duplicate email."""
    # Register first user
    client.post(
        "/api/v1/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "display_name": "Test User"
        }
    )
    
    # Try to register with same email
    response = client.post(
        "/api/v1/register",
        json={
            "email": "test@example.com",
            "password": "password456",
            "display_name": "Another User"
        }
    )
    
    assert response.status_code == 409


def test_login(client):
    """Test user login."""
    # Register user first
    client.post(
        "/api/v1/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "display_name": "Test User"
        }
    )
    
    # Login
    response = client.post(
        "/api/v1/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_login_invalid_password(client):
    """Test login with wrong password."""
    # Register user
    client.post(
        "/api/v1/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "display_name": "Test User"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/v1/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401