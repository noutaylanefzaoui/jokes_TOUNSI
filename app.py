from dotenv import load_dotenv
from jokes_tounsi import create_app

# Load variables from .env into os.environ
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
