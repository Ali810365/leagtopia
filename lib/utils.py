from dotenv import load_dotenv
import os

def generate_keys():
    """Grabs API Key from .env file"""
    load_dotenv()

    api_key = os.getenv("API_KEY")

    return api_key