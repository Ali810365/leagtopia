import json
import time
from lib.client import Client
from lib.utils import generate_keys, get_champions, get_champion

KEY = generate_keys()
REGION = 'americas'
client = Client(KEY, REGION)

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

def main():
    champions = get_champions()

    #for champion in champions['data']:
        #print(f"{champion}| Key: {champions['data'][champion]['key']}")
    
    champions_list = [champion for champion in champions['data']]

    champion = get_champion(champions_list[151], True)




if __name__ == '__main__':
    main()