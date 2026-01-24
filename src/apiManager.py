# Add names for api keys and a menu selection to change between different keys
from dotenv import load_dotenv, set_key
import os 

dotenv_path = ".env"
load_dotenv(dotenv_path)

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

if not api_key or not api_secret:
    print("No api key and secret set.")
    api_key = input("Enter you API key: ").strip()
    api_secret = input("Enter your API secret: ").strip()

    set_key(dotenv_path, "API_KEY", api_key)
    set_key(dotenv_path, "API_SECRET", api_secret)
