# models.py
from extend import db
from datetime import datetime

# =============================================================================
# SUMMONER TABLE
# =============================================================================
# This stores basic info about each player. The puuid is the permanent unique
# identifier from Riot that never changes (unlike summoner names).
#
# Think of this as the "users" table - one row per player.
# =============================================================================

class Summoner(db.Model):
    __tablename__ = 'summoners'
    
    # Primary key - Riot's permanent unique ID for a player
    puuid = db.Column(db.String(100), primary_key=True)
    
    # Riot account info
    summoner_id = db.Column(db.String(100))        # Internal Riot ID (for API calls)
    riot_name = db.Column(db.String(100), nullable=False)  # Display name (e.g., "Faker")
    riot_tag = db.Column(db.String(10), nullable=False)    # Tag (e.g., "KR1")
    region = db.Column(db.String(10), nullable=False)      # Server region (NA1, EUW1, etc.)
    
    # Profile info
    profile_icon_id = db.Column(db.Integer, default=0)
    summoner_level = db.Column(db.Integer, default=1)
    
    # Timestamps - useful for knowing when data was last updated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ==========================================================================
    # RELATIONSHIP: One summoner has MANY match participations
    # ==========================================================================
    # This creates a virtual attribute 'participations' that lets you do:
    #   summoner.participations  ->  returns all MatchParticipant rows for this player
    #
    # backref='summoner' creates the reverse: participant.summoner -> returns Summoner
    # lazy='dynamic' means it returns a query you can filter further, not all results at once
    # ==========================================================================
    participations = db.relationship('MatchParticipant', backref='summoner', lazy='dynamic')
    
    def to_dict(self):
        return {
            'puuid': self.puuid,
            'summoner_id': self.summoner_id,
            'riot_name': self.riot_name,
            'riot_tag': self.riot_tag,
            'region': self.region,
            'profile_icon_id': self.profile_icon_id,
            'summoner_level': self.summoner_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# =============================================================================
# MATCH TABLE
# =============================================================================
# This stores metadata about each match ONCE. Game duration, mode, etc. don't
# change based on which player you're looking at - they're facts about the match.
#
# Key insight: A match happens once, but has 10 participants. We don't want to
# store "game_duration: 1845" ten times - we store it once here.
# =============================================================================

class Match(db.Model):
    __tablename__ = 'matches'
    
    # Primary key - Riot's match ID (e.g., "NA1_4823761234")
    match_id = db.Column(db.String(50), primary_key=True)
    
    # Match metadata (same for all 10 players)
    game_mode = db.Column(db.String(50))           # CLASSIC, ARAM, etc.
    game_type = db.Column(db.String(50))           # MATCHED_GAME, CUSTOM_GAME, etc.
    game_duration = db.Column(db.Integer)          # Duration in seconds
    game_creation = db.Column(db.BigInteger)       # Unix timestamp (milliseconds) when game started
    game_version = db.Column(db.String(50))        # Patch version (e.g., "14.1.1")
    queue_id = db.Column(db.Integer)               # Queue type (420=ranked solo, 400=normal draft, etc.)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ==========================================================================
    # RELATIONSHIP: One match has MANY participants (10 players)
    # ==========================================================================
    participants = db.relationship('MatchParticipant', backref='match', lazy='dynamic')
    
    def to_dict(self):
        return {
            'match_id': self.match_id,
            'game_mode': self.game_mode,
            'game_type': self.game_type,
            'game_duration': self.game_duration,
            'game_creation': self.game_creation,
            'game_version': self.game_version,
            'queue_id': self.queue_id
        }


# =============================================================================
# MATCH PARTICIPANT TABLE (The Junction/Bridge Table)
# =============================================================================
# This is the CORE table that connects summoners to matches and stores all the
# player-specific stats for that game.
#
# Database concept: This is called a "junction table" or "bridge table" because
# it connects two entities (Summoner and Match) in a many-to-many relationship:
#   - One summoner plays in MANY matches
#   - One match has MANY summoners (10 players)
#
# Each row = "What player X did in match Y"
# =============================================================================

class MatchParticipant(db.Model):
    __tablename__ = 'match_participants'
    
    # Auto-incrementing primary key (simpler than composite keys)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ==========================================================================
    # FOREIGN KEYS - These link to the other tables
    # ==========================================================================
    # Foreign key to matches table - which match is this?
    match_id = db.Column(db.String(50), db.ForeignKey('matches.match_id'), nullable=False)
    
    # Foreign key to summoners table - which player is this?
    puuid = db.Column(db.String(100), db.ForeignKey('summoners.puuid'), nullable=False)
    
    # ==========================================================================
    # GAME METADATA- These link to the other tables
    # ==========================================================================
    game_creation = db.Column(db.BigInteger, default=0)
    # ==========================================================================
    # GAME RESULT
    # ==========================================================================
    win = db.Column(db.Boolean)                    # True = won, False = lost
    surrender = db.Column(db.Boolean)              # Did the game end in surrender?
    early_surrender = db.Column(db.Boolean)
    # ==========================================================================
    # CHAMPION INFO
    # ==========================================================================
    champ_id = db.Column(db.Integer)               # Champion ID number
    champ_name = db.Column(db.String(50))          # Champion name (e.g., "Ahri")
    champ_level = db.Column(db.Integer)            # Level at end of game (1-18)
    
    # ==========================================================================
    # POSITION/ROLE
    # ==========================================================================
    lane = db.Column(db.String(20))                # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    role = db.Column(db.String(20))                # SOLO, NONE, CARRY, SUPPORT
    
    # ==========================================================================
    # KDA & COMBAT
    # ==========================================================================
    kills = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    first_blood = db.Column(db.Boolean, default=False)

    # ==========================================================================
    # SUMMONER SPELLS
    # ==========================================================================
    summoner_spell_1 = db.Column(db.Integer, default=0)
    summoner_spell_2 = db.Column(db.Integer, default=0)

    # ==========================================================================
    # ECONOMY
    # ==========================================================================
    gold_earned = db.Column(db.Integer, default=0)
    total_minions_killed = db.Column(db.Integer, default=0)  # CS (creep score)
    
    # ==========================================================================
    # ITEMS - Stored as individual columns (slots 0-6, where 6 is trinket)
    # ==========================================================================
    item0 = db.Column(db.Integer, default=0)
    item1 = db.Column(db.Integer, default=0)
    item2 = db.Column(db.Integer, default=0)
    item3 = db.Column(db.Integer, default=0)
    item4 = db.Column(db.Integer, default=0)
    item5 = db.Column(db.Integer, default=0)
    item6 = db.Column(db.Integer, default=0)       # Trinket slot
    
    # ==========================================================================
    # DAMAGE DEALT
    # ==========================================================================
    total_damage_dealt_to_champions = db.Column(db.Integer, default=0)
    physical_damage_dealt_to_champions = db.Column(db.Integer, default=0)
    magic_damage_dealt_to_champions = db.Column(db.Integer, default=0)
    true_damage_dealt_to_champions = db.Column(db.Integer, default=0)
    
    # ==========================================================================
    # DAMAGE TAKEN
    # ==========================================================================
    total_damage_taken = db.Column(db.Integer, default=0)
    physical_damage_taken = db.Column(db.Integer, default=0)
    magic_damage_taken = db.Column(db.Integer, default=0)
    true_damage_taken = db.Column(db.Integer, default=0)
    
    # ==========================================================================
    # UTILITY STATS
    # ==========================================================================
    total_heal = db.Column(db.Integer, default=0)
    total_heals_on_teammates = db.Column(db.Integer, default=0)
    total_damage_shielded_on_teammates = db.Column(db.Integer, default=0)
    
    # ==========================================================================
    # VISION
    # ==========================================================================
    vision_score = db.Column(db.Integer, default=0)
    wards_placed = db.Column(db.Integer, default=0)
    wards_killed = db.Column(db.Integer, default=0)
    
    # ==========================================================================
    # OBJECTIVES
    # ==========================================================================
    objectives_stolen = db.Column(db.Integer, default=0)
    
    # Timestamp when we stored this record
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ==========================================================================
    # UNIQUE CONSTRAINT
    # ==========================================================================
    # This ensures you can't have duplicate entries for the same player in the 
    # same match. The database will reject any insert that violates this.
    # ==========================================================================
    __table_args__ = (
        db.UniqueConstraint('match_id', 'puuid', name='unique_match_participant'),
        # Indexes for fast lookups
        db.Index('idx_puuid', 'puuid'),
        db.Index('idx_match_id', 'match_id'),
        db.Index('idx_puuid_created', 'puuid', 'created_at'),
        db.Index('idx_champ', 'champ_id'),
    )
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'match_id': self.match_id,
            'puuid': self.puuid,
            'win': self.win,
            'surrender': self.surrender,
            'champ_id': self.champ_id,
            'champ_name': self.champ_name,
            'champ_level': self.champ_level,
            'lane': self.lane,
            'role': self.role,
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'first_blood': self.first_blood,
            'gold_earned': self.gold_earned,
            'total_minions_killed': self.total_minions_killed,
            'item0': self.item0,
            'item1': self.item1,
            'item2': self.item2,
            'item3': self.item3,
            'item4': self.item4,
            'item5': self.item5,
            'item6': self.item6,
            'total_damage_dealt_to_champions': self.total_damage_dealt_to_champions,
            'physical_damage_dealt_to_champions': self.physical_damage_dealt_to_champions,
            'magic_damage_dealt_to_champions': self.magic_damage_dealt_to_champions,
            'true_damage_dealt_to_champions': self.true_damage_dealt_to_champions,
            'total_damage_taken': self.total_damage_taken,
            'physical_damage_taken': self.physical_damage_taken,
            'magic_damage_taken': self.magic_damage_taken,
            'true_damage_taken': self.true_damage_taken,
            'total_heal': self.total_heal,
            'total_heals_on_teammates': self.total_heals_on_teammates,
            'total_damage_shielded_on_teammates': self.total_damage_shielded_on_teammates,
            'vision_score': self.vision_score,
            'wards_placed': self.wards_placed,
            'wards_killed': self.wards_killed,
            'objectives_stolen': self.objectives_stolen,
            'summoner_spell_1': self.summoner_spell_1,
            'summoner_spell_2': self.summoner_spell_2,
            'early_surrender': self.early_surrender,
            'game_creation': self.game_creation,
        }
    
    def to_dict_with_match(self):
        """Include match metadata in the response (for frontend convenience)"""
        data = self.to_dict()
        if self.match:
            data['game_mode'] = self.match.game_mode
            data['game_duration'] = self.match.game_duration
            data['game_creation'] = self.match.game_creation
            data['queue_id'] = self.match.queue_id
        return data


# =============================================================================
# QUICK REFERENCE: How the relationships work
# =============================================================================
#
# Get a summoner's match history:
#   summoner = Summoner.query.get(puuid)
#   recent_games = summoner.participations.order_by(MatchParticipant.created_at.desc()).limit(20).all()
#
# Get all participants in a match:
#   match = Match.query.get(match_id)
#   all_players = match.participants.all()  # Returns 10 MatchParticipant objects
#
# Get match details from a participation:
#   participant = MatchParticipant.query.first()
#   print(participant.match.game_duration)  # Access match data via relationship
#   print(participant.summoner.riot_name)   # Access summoner data via relationship
#
# =============================================================================
