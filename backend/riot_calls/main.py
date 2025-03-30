from dotenv import load_dotenv
import os
import requests
from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from typing import Dict, Any, Union, List

load_dotenv()

api_key = os.environ.get('riot_api_key')

def get_puuid(gameName=None, tagLine=None, region='americas'):
    
    #link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'

    #response = requests.get(link)
    
    """ Gets a puuid from either summonerId or riot id + tag. Returns a str of the puuid

        Args:   
            
            gameName (str; optional) - Riot ID, None by default
            tagLine (str; optional) - Riot Tag, None by default
            region (str; optional) - Summoner ID, americas by default
    """
    

    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('puuid', None)
    elif response.status_code == 404:
        return 0
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    


def get_summoner_id_from_puuid(puuid, region='na1'):
    """
    Fetches the Summoner ID from a given PUUID.

    Args:
        puuid (str): The player's PUUID.
        region (str): The Riot API region (default: na1).

    Returns:
        str: The Summoner ID if found, otherwise None.
    """

    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('id', None)  # 'id' is the Summoner ID
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
'''
data = requests.get_json()  # This turns the JSON into a Python dict

summonerID = data.get("summonerID")
riot_tag = data.get("riot_tag")
region = data.get("region")

print("Received from frontend:", summonerID, riot_tag, region)
'''

def get_summoner_info(puuid:str = None,region:str = None, api:str = api_key) -> Dict[str, Any]:
    '''
    Retrieves summoner icon, summoner level, id, and account id, by using a puuid and an api-key.

    When you put in a puuid, you will get back a JSON from riot containing: id, accountId, puuid,
    profileIconId, revisionDate, summonerLevel.

    Args:
        puuid (str): PUUID obtained from a user
        region (str): The region used in the search-bar (Not the spelled out version like Americas)
        api (str): Riot API key that we are using (In .env)
    

    Returns:
        JSON: JSON from Riot
    '''
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return{'status': response.status_code, 'message': response.text}

#print(get_summoner_info('X7X-J_Tus9r4DcQSs7wvQr1r-vzzU3sK-iZ9RbzzAYaxgAZpzR3f-HfuvIYkQK-kJoitltvYm6rPUw', 'NA1'))

#print(get_puuid('Doublelift','NA1'))