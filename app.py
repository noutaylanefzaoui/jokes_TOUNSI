from dotenv import load_dotenv
from jokes_tounsi import create_app, db
from jokes_tounsi import models  # so migrations see all models


# Load variables from .env into os.environ
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
