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
    match_id1 = db.Column(db.JSON)
    match_id2 = db.Column(db.JSON)
    match_id3 = db.Column(db.JSON)
    match_id4 = db.Column(db.JSON)
    match_id5 = db.Column(db.JSON)
    match_id6 = db.Column(db.JSON)
    match_id7 = db.Column(db.JSON)
    match_id8 = db.Column(db.JSON)
    match_id9 = db.Column(db.JSON)
    match_id10 = db.Column(db.JSON)
    match_id11 = db.Column(db.JSON)
    match_id12 = db.Column(db.JSON)
    match_id13 = db.Column(db.JSON)
    match_id14 = db.Column(db.JSON)
    match_id15 = db.Column(db.JSON)
    match_id16 = db.Column(db.JSON)
    match_id17 = db.Column(db.JSON)
    match_id18 = db.Column(db.JSON)
    match_id19 = db.Column(db.JSON)
    match_id20 = db.Column(db.JSON)
    
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
    


