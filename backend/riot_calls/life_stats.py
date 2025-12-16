from stats import *



breh = retrieve_match_history("X7X-J_Tus9r4DcQSs7wvQr1r-vzzU3sK-iZ9RbzzAYaxgAZpzR3f-HfuvIYkQK-kJoitltvYm6rPUw", 'americas', 0, 20)

#print(breh)

game = get_match_data_from_id(breh[0], 'americas')

#print(game)

def process_match_get_life_stats(match_json,puuid):
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


    #game_mode = info.get('gameMode', 'Unknown')

    game_mode = info['gameMode']

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
    total_teammate_shielding = player['totalDamageShieldedOnTeammates']
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

    
    #you can get bans with pick orders with teams variable.

    match_data = {
    "game_mode" : game_mode,
    "win": win,
    "kills": kills,
    "deaths": deaths,
    "assists": assists,
    "champ_id": champ,
    "champ_name": champ_name,
    "lane": lane,
}
    return match_data


here = process_match_get_life_stats(game, "X7X-J_Tus9r4DcQSs7wvQr1r-vzzU3sK-iZ9RbzzAYaxgAZpzR3f-HfuvIYkQK-kJoitltvYm6rPUw")
#print(here)

totals = {}
#if here['win'] == False:
totals["wins"] = 0
totals["losses"] = 0
totals['kills'] = 0
totals['deaths'] = 0
totals['assists'] = 0
#print(totals)
champ_totals = {}
champ_wins = {}
min_matches = 2


for match in breh:
    
    #print(match)
    match_data = get_match_data_from_id(match, 'americas')
    #print(match_data)
    temp = process_match_get_life_stats(match_data, "X7X-J_Tus9r4DcQSs7wvQr1r-vzzU3sK-iZ9RbzzAYaxgAZpzR3f-HfuvIYkQK-kJoitltvYm6rPUw")
    #print(temp)
    if temp['win'] == True:
        #print(temp['win'])
        totals["wins"] += 1
    else:
        #print(temp['win'])
        totals['losses'] += 1

    totals['kills'] += temp['kills']
    totals['deaths'] += temp['deaths']
    totals['assists'] += temp['assists']

    if temp['champ_name'] in champ_totals:
        #print(temp['champ_name'])
        champ_totals[temp['champ_name']] += 1
        #print(totals[temp['champ_name']])
        if temp['win'] == True:
            #print(f"{temp['champ_name']}: win")
            champ_wins[temp['champ_name']] += 1
    
    if temp['champ_name'] not in champ_totals:
        champ_totals[temp['champ_name']] = 1

        if temp['win'] == True:
            #print(f"{temp['champ_name']}: win ------ first seen")
            champ_wins[temp['champ_name']] = 1
        else:
            champ_wins[temp['champ_name']] = 0
    
    '''
    if temp['champ_name'] in champ_totals:
        #print(temp['champ_name'])
        champ_totals[temp['champ_name']] += 1
        #print(totals[temp['champ_name']])
        if temp['win'] == True:
            print(f"{temp['champ_name']}: win")
            champ_wins[temp['champ_name']] += 1
    '''
#print(totals)

totals['kda'] = (totals['kills'] + totals['assists'])/totals['deaths']

#print(champ_totals)
sorted_champ_by_matches = sorted(champ_totals, key=champ_totals.get, reverse=True)
print(f'Champs by matches played: {sorted_champ_by_matches}')
totals['most_played_champs'] = ",".join(sorted_champ_by_matches[:5]) #the 5 gets the 5 most played champs
#print(totals)


#print(champ_wins)


champ_winrates = {}
for champ, wins in champ_wins.items():
    #print(champ, wins)
    if champ_totals[champ] > 2:
        #print(champ, wins)
        champ_winrates[champ] = wins/champ_totals[champ]

print(f'champion winrates: {champ_winrates}')
sorted_winrates_worse = sorted(champ_winrates, key=champ_totals.get, reverse=True)
sorted_winrates_best = sorted(champ_winrates, key=champ_totals.get)
print(f'{sorted_winrates_worse}')
print(sorted_winrates_best)

totals['best_champs'] = ",".join(sorted_winrates_best[:3]) #for both of these change the number to get the number of spot for that respective theme
totals['worse_champs'] = ",".join(sorted_winrates_worse[:3])

print(totals)
