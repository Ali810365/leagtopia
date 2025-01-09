from dotenv import load_dotenv
from lib.champion import Champion
from lib.client import Client
import json
import os


champions = Champion('15.1.1')

def generate_keys():
    """Grabs API Key from .env file"""
    load_dotenv()

    api_key = os.getenv("API_KEY")

    return api_key

def get_champions(write_to_file=False):
    response = champions.get_champions()
    if write_to_file:
        with open("output/na_champions.json", 'w') as f:
            f.write(json.dumps(response, indent=3))
    
    return response

def get_champion(champion:str, write_to_file=False):

    response = champions.get_champion(champion)
    key = response['data'][champion]['key']


    if write_to_file:
        with open(f"output/{key}.json", "w") as f:
            f.write(json.dumps(response, indent=3))

    return response