import requests

class Client:
    def __init__(self, api_key:str, riot_region:str):
        self.API_KEY = api_key
        self.RIOT_REGION = riot_region
    
    def return_api_key(self):
        return self.API_KEY
    
    def request_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": self.API_KEY
        }
    
    def get_account_by_riot_id(self, game_name:str, tag_line:str):
        endpoint = f"https://{self.RIOT_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        headers = self.request_headers()

        response = requests.get(endpoint, headers=headers)

        return response.json()
    
    def spectate_game(self, puuid:str, platform_region:str):
        endpoint = f"https://{platform_region}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
        headers = self.request_headers()

        response = requests.get(endpoint, headers=headers)

        return response.json()



