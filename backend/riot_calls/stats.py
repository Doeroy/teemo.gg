from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.environ.get('riot_api_key')

def get_match_history(puuid=None, region='americas', start=0, count= 20):
    
    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'lol/match/v5/matches/by-puuid/{puuid}/ids'
    query_params = f'?start={start}&count={count}'

    response = requests.get(root_url + endpoint + query_params + '&api_key='+ api_key)
    return response.json()

breh = get_match_history('XuQC9ILJ5989b1BnraT6PvIUUnCT7lTuM8N4itF0wXllxOQkWBi2ByCekmd3BVofFn0McwKgxJUw1g', 'americas', 0, 20)

print(breh)

def get_match_data_from_id(matchId= None, region=None):
    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'lol/match/v5/matches/{matchId}'
    #print(root_url + endpoint + '?api_key='+ api_key)

    response = requests.get(root_url + endpoint + '?api_key='+ api_key)

    return response.json()

game = get_match_data_from_id(breh[0], 'americas')

#print(game)

def process_match_json(match_json,puuid):
    metadata = match_json['metadata']
    info = match_json['info']
    players = info['participants']

    match_id = metadata['matchId']
    participants = metadata['participants']
    teams = info['teams']
    player = players[participants.index(puuid)]

    game_creation = info['gameCreation']
    game_duration = info['gameDuration']
    game_start_timestamp = info['gameStartTimestamp']
    game_end_timestamp = info['gameEndTimestamp']
    patch_version = info['gameVersion']

    assists = player['assists']
    champ = player['championId']
    champ_name = player['championName']
    champ_lvl = player['champLevel']
    kayn_form = player['championTransform']
    deaths = player['deaths']
    goldcount = player['goldEarned']
    item0 = player['item0']
    item1 = player['item1']
    item2 = player['item2']
    item3 = player['item3']
    item4 = player['item4']
    item5 = player['item5']
    item6 = player['item6']
    kills = player['kills']
    first_blood = player['firstBloodKill']
    lane = player['lane']
    magic_dmg_dealt = player['magicDamageDealt']
    magic_dmg_dealt_to_champion = player['magicDamageDealtToChampions']
    magic_dmg_taken = player['magicDamageTaken']
    nminions_killed = player['neutralMinionsKilled']
    objectives_stolen = player['objectivesStolen']
    objective_stolen_assists = player['objectivesStolenAssists']
    physical_dmg_dealt = player['physicalDamageDealt']
    physical_dmg_dealt_to_champion = player['physicalDamageDealtToChampions']
    physical_dmg_taken = player['physicalDamageTaken']
    riot_id = player['riotIdGameName']
    riot_tag = player['riotIdTagline']                       
    summoner1_id = player['summoner1Id']
    summoner2_id = player['summoner2Id']
    summoner_id = player['summonerId']
    summoner_lvl = player['summonerLevel']
    summoner_name = player['summonerName']
    team_side = player['teamId']
    most_likely_role = player['teamPosition']
    total_dmg_dealt = player['totalDamageDealt']
    total_dmg_dealt_to_champions = player['totalDamageDealtToChampions']
    total_damage_taken = player['totalDamageTaken']
    total_teammate_healing = player['totalHealsOnTeammates']
    total_minions_killed = player['totalMinionsKilled']
    true_damage_dealt = player['trueDamageDealt']
    true_damage_dealt_to_champions = player['trueDamageDealtToChampions']
    true_damage_taken = player['trueDamageTaken']
    vision_score = player['visionScore']
    wards_placed = player['wardsPlaced']
    wards_killed = player['wardsKilled']
    early_surrender = player['gameEndedInEarlySurrender']
    surrender = player['gameEndedInSurrender']
    win = player['win']

    '''
    you can get bans with pick orders with teams variable.
    
    
    
    
    '''


    match_data = {
    "win": win,
    "kills": kills,
    "deaths": deaths,
    "assists": assists,
    "game_end_timestamp": game_end_timestamp,
    "champ": champ,
    "champ_name": champ_name,
    "champ_lvl": champ_lvl,
    "goldcount": goldcount,
    "item0": item0,
    "item1": item1,
    "item2": item2,
    "item3": item3,
    "item4": item4,
    "item5": item5,
    "item6": item6,
    "first_blood": first_blood,
    "lane": lane,
    "magic_dmg_dealt_to_champions": magic_dmg_dealt_to_champion,
    "magic_dmg_taken": magic_dmg_taken,
    "objectives_stolen": objectives_stolen,
    "physical_dmg_dealt_to_champions": physical_dmg_dealt_to_champion,
    "physical_dmg_taken": physical_dmg_taken,
    "total_dmg_dealt_to_champions": total_dmg_dealt_to_champions,
    "total_damage_taken": total_damage_taken,
    "total_teammate_healing": total_teammate_healing,
    "total_minions_killed": total_minions_killed,
    "true_dmg_dealt_to_champions": true_damage_dealt_to_champions,
    "true_dmg_taken": true_damage_taken,
    "vision_score": vision_score,
    "wards_placed": wards_placed,
    "wards_killed": wards_killed,
    "surrender": surrender
}
    return match_data


filter = process_match_json(game,'XuQC9ILJ5989b1BnraT6PvIUUnCT7lTuM8N4itF0wXllxOQkWBi2ByCekmd3BVofFn0McwKgxJUw1g')

#print(f'kills: {filter[0]} | deaths: {filter[1]}')
#print(filter)