# models.py
from extend import db  # Import db from extensions

class SummonerProfile(db.Model):
    __tablename__ = 'summoner_prof_test1'  # Make sure this matches your table name
    summonerID = db.Column(db.String(50))
    riot_id = db.Column(db.String(100))
    riot_tag = db.Column(db.String(10))
    puuid = db.Column(db.String(100), primary_key=True)
    region = db.Column(db.String(10))

    def to_dict(self):
        return {
            'summonerID': self.summonerID,
            'riot_id': self.riot_id,
            'riot_tag': self.riot_tag,
            'puuid': self.puuid,
            'region': self.region
        }
    
class SummonerStats(db.Model):
    
    __tablename__ = "match_history"

    puuid = db.Column(db.String(100), primary_key=True)
    match_id1 = db.Column(db.String(255))
    match_id2 = db.Column(db.String(255))
    match_id3 = db.Column(db.String(255))
    match_id4 = db.Column(db.String(255))
    match_id5 = db.Column(db.String(255))
    match_id6 = db.Column(db.String(255))
    match_id7 = db.Column(db.String(255))
    match_id8 = db.Column(db.String(255))
    match_id9 = db.Column(db.String(255))
    match_id10 = db.Column(db.String(255))
    match_id11 = db.Column(db.String(255))
    match_id12 = db.Column(db.String(255))
    match_id13 = db.Column(db.String(255))
    match_id14 = db.Column(db.String(255))
    match_id15 = db.Column(db.String(255))
    match_id16 = db.Column(db.String(255))
    match_id17 = db.Column(db.String(255))
    match_id18 = db.Column(db.String(255))
    match_id19 = db.Column(db.String(255))
    match_id20 = db.Column(db.String(255))
    
    def to_dict(self):
        return{
            'puuid' : self.puuid,
            'match_id1' : self.match_id1,
            'match_id2' : self.match_id2,
            'match_id3' : self.match_id3,
            'match_id4' : self.match_id4,
            'match_id5' : self.match_id5,
            'match_id6' : self.match_id6,
            'match_id7' : self.match_id7,
            'match_id8' : self.match_id8,
            'match_id9' : self.match_id9,
            'match_id10' : self.match_id10,
            'match_id11' : self.match_id11,
            'match_id12' : self.match_id12,
            'match_id13' : self.match_id13,
            'match_id14' : self.match_id14,
            'match_id15' : self.match_id15,
            'match_id16' : self.match_id16,
            'match_id17' : self.match_id17,
            'match_id18' : self.match_id18,
            'match_id19' : self.match_id19,
            'match_id20' : self.match_id20
        }
    

class MatchStats(db.Model):

    __tablename__ = "match_stats"

    puuid = db.Column(db.String(100), primary_key=True)
    match_id = db.Column(db.String(255), primary_key=True)
    game_mode = db.Column(db.String(255)) 
    win = db.Column(db.Integer)
    kills = db.Column(db.Integer) 
    deaths = db.Column(db.Integer) 
    assists = db.Column(db.Integer) 
    game_duration = db.Column(db.Integer) 
    champ_id = db.Column(db.Integer) 
    champ_name = db.Column(db.String(255)) 
    champ_lvl = db.Column(db.Integer) 
    goldcount = db.Column(db.Integer) 
    item0 = db.Column(db.Integer) 
    item1 = db.Column(db.Integer) 
    item2 = db.Column(db.Integer) 
    item3 = db.Column(db.Integer) 
    item4 = db.Column(db.Integer) 
    item5 = db.Column(db.Integer) 
    item6 = db.Column(db.Integer) 
    first_blood = db.Column(db.Boolean) 
    lane = db.Column(db.String(255))
    magic_dmg_dealt_to_champions = db.Column(db.Integer) 
    magic_dmg_taken = db.Column(db.Integer) 
    physical_dmg_dealt_to_champions = db.Column(db.Integer) 
    physical_dmg_taken = db.Column(db.Integer) 
    true_dmg_dealt_to_champions = db.Column(db.Integer) 
    true_dmg_taken = db.Column(db.Integer) 
    total_dmg_dealt_to_champions = db.Column(db.Integer) 
    total_damage_taken = db.Column(db.Integer) 
    total_teammate_healing = db.Column(db.Integer) 
    total_teammate_shielding = db.Column(db.Integer) 
    total_minions_killed = db.Column(db.Integer) 
    objectives_stolen = db.Column(db.Integer) 
    vision_score = db.Column(db.Integer) 
    wards_placed = db.Column(db.Integer) 
    wards_killed = db.Column(db.Integer) 
    surrender = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "puuid": self.puuid,
            "match_id": self.match_id,
            "game_mode": self.game_mode,
            "win": self.win,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "game_duration": self.game_duration,
            "champ_id": self.champ_id,
            "champ_name": self.champ_name,
            "champ_lvl": self.champ_lvl,
            "goldcount": self.goldcount,
            "item0": self.item0,
            "item1": self.item1,
            "item2": self.item2,
            "item3": self.item3,
            "item4": self.item4,
            "item5": self.item5,
            "item6": self.item6,
            "lane": self.lane,
            "first_blood": self.first_blood,
            "magic_dmg_dealt_to_champions": self.magic_dmg_dealt_to_champions,
            "magic_dmg_taken": self.magic_dmg_taken,
            "physical_dmg_dealt_to_champions": self.physical_dmg_dealt_to_champions,
            "physical_dmg_taken": self.physical_dmg_taken,
            "true_dmg_dealt_to_champions": self.true_dmg_dealt_to_champions,
            "true_dmg_taken": self.true_dmg_taken,
            "total_dmg_dealt_to_champions": self.total_dmg_dealt_to_champions,
            "total_damage_taken": self.total_damage_taken,
            "total_teammate_healing": self.total_teammate_healing,
            "total_teammate_shielding": self.total_teammate_shielding,
            "total_minions_killed": self.total_minions_killed,
            "objectives_stolen": self.objectives_stolen,
            "vision_score": self.vision_score,
            "wards_placed": self.wards_placed,
            "wards_killed": self.wards_killed,
            "surrender": self.surrender
        }


