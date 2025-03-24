from dotenv import load_dotenv
import os
import requests


load_dotenv()

api_key = os.environ.get('riot_api_key')


def get_puuid(gameName=None, tagLine=None, region='americas'):
    
    #link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'

    #response = requests.get(link)
    
    """ Gets a puuid from either summonerId or riot id + tag. Returns a str of the puuid

        Args:   
            summonerId (str; optional) - Summoner ID, None by default
            gameName (str; optional) - Riot ID, None by default
            tagLine (str; optional) - Riot Tag, None by default
            region (str; optional) - Summoner ID, americas by default
    """

    #if summonerId is not None:
    #    root_url = f'https://{region}.api.riotgames.com/'
    #    endpoint = 'lol/summoner/v4/summoners/'
        
    #    print(root_url + endpoint + summonerId + '?api_key='+ api_key)
    #    response = requests.get(root_url + endpoint + summonerId + '?api_key='+ api_key)

    #    return response.json()['puuid']
    
    #else:
    summonerId=None

    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'

    response = requests.get(root_url + endpoint + summonerId + '?api_key='+ api_key)

    return response.json()['puuid']
    


