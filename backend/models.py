# models.py
from extend import db  # Import db from extensions

class SummonerProfile(db.Model):
    __tablename__ = 'summoner_prof_test1'  # Make sure this matches your table name

    summonerID = db.Column(db.String(50), primary_key=True)
    riot_id = db.Column(db.String(45), nullable=False)
    riot_tag = db.Column(db.String(45), nullable=False)
    puuid = db.Column(db.String(45), unique=True, nullable=False)
    region = db.Column(db.String(45), nullable=False)

    def to_dict(self):
        return {
            'summonerID': self.summonerID,
            'riot_id': self.riot_id,
            'riot_tag': self.riot_tag,
            'puuid': self.puuid,
            'region': self.region
        }


