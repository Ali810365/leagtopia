import os
import json
import time
from dotenv import load_dotenv
from lib.client import Client
from lib.champion import Champion
from azure.cosmos import exceptions
from db.cosmos_wrapper import CosmosWrapper

load_dotenv()

API_KEY = os.getenv("API_KEY")
REGION = 'americas'
champions = Champion('15.1.1')
client = Client(API_KEY, REGION)


def get_champions(write_to_file=False):
    response = champions.get_champions()
    if write_to_file:
        with open("output/na_champions.json", 'w') as f:
            f.write(json.dumps(response, indent=3))
    
    return response

def get_champion(champion:str, write_to_file=False):

    response = champions.get_champion(champion)
    key = response['data'][champion]['key']

    champion_data = {
        "id": key,
        "champion": response['data'][champion]
    }


    if write_to_file:
        with open(f"output/{key}.json", "w") as f:
            f.write(json.dumps(champion_data, indent=3))

    return champion_data

def add_all_champions_to_cosmos():
    cosmos = CosmosWrapper({})
    champions = get_champions()

    #for champion in champions['data']:
        #print(f"{champion}| Key: {champions['data'][champion]['key']}")
    

    champions_list = [champion for champion in champions['data']]

    try:
        counter = 0
        for champion in champions_list:
            try:
                champion = get_champion(champion)
                cosmos.create_item(champion)
                counter+=1
                print(f"Progress: {counter}/{len(champions_list)}")
            except exceptions.CosmosResourceExistsError:
                print(f"Progress: {counter/len(champions_list)} | Resource already exists")
                continue
    except exceptions.CosmosResourceExistsError:
        print('ERROR: Resource already exists')

def get_game_duration():
    def convert_ms(ms):
        # Convert milliseconds to seconds
        seconds = ms // 1000
        # Calculate minutes and remaining seconds
        minutes = seconds // 60
        seconds = seconds % 60
        # Format as minutes:seconds (e.g., 02:30)
        return f"{minutes:02}:{seconds:02}"
    
    with open("./output/sample_spectate_game_response.json", "r") as f:
        data = json.load(f)

    start_time = data['gameStartTime']
    current_time = round(time.time() * 1000)

    elapsed_time = current_time - start_time

    elapsed_time_in_minutes = convert_ms(elapsed_time)

    print(elapsed_time_in_minutes)

def get_account():
    account = client.get_account_by_riot_id("Strompest", "UCI")
    with open("./output/sample_get_account_response.json", "w") as f:
        f.write(json.dumps(account, indent=3))
    
    return account

def spectate_game():
    puuid = get_account()['puuid']

    game = client.spectate_game(puuid, 'na1')
    with open("./output/sample_spectate_game_response.json", "w") as f:
        f.write(json.dumps(game, indent=3))

    return game

def get_champion_from_cosmos(champion_key:str):
    cosmos = CosmosWrapper({})

    item = cosmos.read_item(champion_key, champion_key)

    return item