import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from jokes_tounsi.config import DevelopmentConfig
from jokes_tounsi import create_app, db
from jokes_tounsi import models

# Determine config
env = os.getenv("FLASK_ENV", "development")
if env == "production":
    from jokes_tounsi.config import ProductionConfig
    config = ProductionConfig
else:
    config = DevelopmentConfig

# Create app
app = create_app(config)

if __name__ == "__main__":
    # Run development server
    app.run(debug=config.DEBUG, host="0.0.0.0", port=5000)