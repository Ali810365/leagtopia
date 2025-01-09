import requests

class Champion:
    def __init__(self, version:str):
        self.version = version
    
    def get_champions(self):
        endpoint = f'https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json'
        response = requests.get(endpoint)

        return response.json()
    def get_champion(self, champion:str):
        endpoint = f'https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion/{champion}.json'

        response = requests.get(endpoint)

        return response.json()
