# jokesTOUNSI

jokesTOUNSI is a Flask-based REST API for managing and sharing Tunisian jokes. It allows users to browse jokes, contribute their own, and securely authenticate via Google OAuth.

## Features

-   **Authentication**: Secure login utilizing Google OAuth 2.0 and JWT (JSON Web Tokens).
-   **Jokes Management**: Endpoints to list, create, update, and delete jokes.
-   **Documentation**: Interactive API documentation via Swagger UI.
-   **Docker Support**: Fully containerized application for easy deployment using Docker Compose.
-   **Database**: SQLite database for persistent storage.

## Endpoints

The API is versioned (v1). Key endpoints include:

-   `GET /api/v1/auth/google`: Initiate Google OAuth login.
-   `GET /api/v1/jokes`: List all jokes (with pagination and filtering).
-   `POST /api/v1/jokes`: Create a new joke (Requires authentication).
-   `GET /api/v1/docs`: Access Swagger UI documentation.
-   `GET /health`: Health check endpoint.

## Prerequisites

-   **Python 3.13+** (for local development)
-   **Docker Engine & Docker Compose** (for containerized deployment)
-   **Google Cloud Project**: You need a Google Cloud project with OAuth 2.0 credentials (`CLIENT_ID` and `CLIENT_SECRET`).

## Configuration

Create a `.env` file in the root directory based on the following template:

```ini
FLASK_APP=app.py
FLASK_ENV=development  # Use 'production' for deployment
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=sqlite:///jokes_dev.db

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OAUTH2_REDIRECT_URI=http://127.0.0.1:5000/api/v1/auth/google/callback
```

> [!IMPORTANT]
> The `OAUTH2_REDIRECT_URI` must match exactly what is configured in your Google Cloud Console.

## Installation & Running

### Option 1: Docker (Recommended)

1.  **Build and Start:**
    ```bash
    docker compose up --build -d
    ```
    The application will be available at `http://127.0.0.1:5000`.

2.  **View Logs:**
    ```bash
    docker compose logs -f
    ```

3.  **Stop:**
    ```bash
    docker compose down
    ```

### Option 2: Local Python Environment

1.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Application:**
    ```bash
    python app.py
    ```

## Testing

Run the test suite using pytest:

```bash
pytest
```

## API Documentation

Once the server is running, visit the Swagger UI to explore and test the API endpoints:

[http://127.0.0.1:5000/api/v1/docs](http://127.0.0.1:5000/api/v1/docs)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
