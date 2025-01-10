import json
import time
from lib.client import Client
from lib.utils import get_champions, get_champion, get_champion_from_cosmos
from azure.cosmos import exceptions
from db.cosmos_wrapper import CosmosWrapper


def main():
    with open('./output/sample_spectate_game_response.json', 'r') as f:
        game = json.load(f)
    
    for player in game['participants']:
        key = player['championId']
        champion = get_champion_from_cosmos(str(key))
    
        player['championId'] = champion[0]['champion']['name']
    
    with open('./output/sample_spectate_game_response_fixed.json', 'w') as f:
        f.write(json.dumps(game, indent=3))

if __name__ == '__main__':
    main()