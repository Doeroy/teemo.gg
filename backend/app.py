import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text
from extend import db
from flask_cors import CORS

# Import the NEW normalized models
from models import Summoner, Match, MatchParticipant

# Riot API helper functions
from riot_calls.main import get_puuid, get_summoner_id_from_puuid, get_summoner_info
from riot_calls.stats import get_match_data_from_id, retrieve_match_history, process_match_json

# =============================================================================
# APP CONFIGURATION
# =============================================================================

load_dotenv()
print("DB_HOST =", os.getenv("DB_HOST"))

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_routing_region(region):
    """
    Convert server region to Riot API routing region.
    Riot has regional routing for match-v5 endpoints.
    """
    if region == 'NA1':
        return 'americas'
    elif region in ('EUW1', 'EUNE1'):
        return 'europe'
    elif region in ('KR', 'JP1', 'VN2'):
        return 'asia'
    else:
        return 'sea'


# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================

@app.route('/test_db')
def test_db():
    """Test database connection"""
    try:
        db.session.execute(text('SELECT 1'))
        return "Database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"


# =============================================================================
# SUMMONER ENDPOINTS
# =============================================================================

@app.route('/search', methods=['POST'])
def search():
    """
    Quick search - gets puuid from Riot API without saving to database.
    Use this for autocomplete/validation before full search.
    """
    data = request.get_json()
    summoner_name = data['summonerID']
    tag_line = data['riot_tag']
    region = data['region']
    
    puuid = get_puuid(gameName=summoner_name, tagLine=tag_line)
    
    return jsonify({
        'summonerID': get_summoner_id_from_puuid(puuid),
        'riot_id': summoner_name,
        'riot_tag': tag_line,
        'puuid': puuid,
        'region': region
    })


@app.route('/search_and_add_summoner', methods=['POST'])
def search_and_add_summoner():
    """
    Search for a summoner via Riot API and save/update them in our database.
    Flow:
    1. Get puuid from Riot Account API
    2. Get profile info from Riot Summoner API
    3. Insert or update summoner in our database
    4. Return summoner data to frontend
    """
    try:
        data = request.get_json()
        print("Incoming data:", data)
        
        # Validate required fields
        required_fields = ['summonerID', 'riot_id', 'riot_tag', 'puuid', 'region']
        if not all(key in data for key in required_fields):
            return jsonify({"error": "Missing data in request!"}), 400
        
        summoner_name = data['summonerID']
        tag_line = data['riot_tag']
        region = data['region']
        
        # Step 1: Get puuid from Riot API
        real_puuid = get_puuid(gameName=summoner_name, tagLine=tag_line)
        if real_puuid == 0:
            return jsonify({'success': False, 'error': 'not_found'}), 404
        
        print(f"PUUID: {real_puuid}")
        
        # Step 2: Get summoner profile from Riot API
        s_dict = get_summoner_info(real_puuid, region)
        
        if 'status' in s_dict:
            return jsonify({
                'success': False,
                'error': f"Riot API error: {s_dict.get('message', 'Unknown error')}"
            }), 400
        
        # Get summoner_id (fallback if missing)
        summoner_id = s_dict.get('id')
        if not summoner_id:
            summoner_id = get_summoner_id_from_puuid(real_puuid, region)
            if not summoner_id:
                summoner_id = "unknown"
        
        # Step 3: Insert or update summoner in database
        # =====================================================================
        # This is called an "UPSERT" - insert if new, update if exists
        # =====================================================================
        existing_summoner = Summoner.query.get(real_puuid)
        
        if existing_summoner:
            # Update existing summoner
            existing_summoner.summoner_id = summoner_id
            existing_summoner.riot_name = summoner_name
            existing_summoner.riot_tag = tag_line
            existing_summoner.region = region
            existing_summoner.profile_icon_id = s_dict.get('profileIconId', 0)
            existing_summoner.summoner_level = s_dict.get('summonerLevel', 1)
            print(f"Updated existing summoner: {summoner_name}#{tag_line}")
        else:
            # Create new summoner
            new_summoner = Summoner(
                puuid=real_puuid,
                summoner_id=summoner_id,
                riot_name=summoner_name,
                riot_tag=tag_line,
                region=region,
                profile_icon_id=s_dict.get('profileIconId', 0),
                summoner_level=s_dict.get('summonerLevel', 1)
            )
            db.session.add(new_summoner)
            print(f"Added new summoner: {summoner_name}#{tag_line}")
        
        db.session.commit()
        
        # Step 4: Return response
        return jsonify({
            'success': True,
            'error': None,
            'id': summoner_id,
            'puuid': real_puuid,
            'region': region,
            'icon': s_dict.get('profileIconId', 0),
            'level': s_dict.get('summonerLevel', 1),
            'summonerName': summoner_name,
            'tag_line': tag_line
        })
        
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'success': False, 'error': f"Failed to add summoner: {str(e)}"}), 400


@app.route('/search_and_send_summoner', methods=['GET'])
def retrieve_summoner_info():
    """
    Retrieve a summoner from our database by name and tag.
    If found, also fetches fresh profile data from Riot API.
    """
    try:
        summoner_name = request.args.get('summoner_name')
        tag_line = request.args.get('riot_tag')
        print(f'Looking up summoner: {summoner_name}#{tag_line}')
        
        # Query using the new model
        summoner = Summoner.query.filter_by(
            riot_name=summoner_name,
            riot_tag=tag_line
        ).first()
        
        if not summoner:
            return jsonify({"message": "Could not find summoner in database"}), 404
        
        # Fetch fresh data from Riot API
        s_dict = get_summoner_info(summoner.puuid, summoner.region)
        
        if 'status' in s_dict:
            return jsonify({
                "error": f"Riot API error: {s_dict.get('message', 'Unknown error')}"
            }), 400
        
        # Get summoner_id (fallback if missing)
        summoner_id = s_dict.get('id')
        if not summoner_id:
            summoner_id = get_summoner_id_from_puuid(summoner.puuid, summoner.region)
            if not summoner_id:
                summoner_id = "unknown"
        
        return jsonify({
            'id': summoner_id,
            'icon': s_dict.get('profileIconId', 0),
            'level': s_dict.get('summonerLevel', 1),
            'summonerName': summoner_name,
            'tag_line': tag_line,
            'puuid': summoner.puuid,
            'region': summoner.region,
        }), 200
        
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Failed to retrieve summoner: {str(e)}"}), 400


@app.route('/summoners', methods=['GET'])
def get_summoners():
    """Get all summoners (for testing/debugging)"""
    try:
        summoners = Summoner.query.all()
        return jsonify([s.to_dict() for s in summoners])
    except Exception as e:
        print("/summoners error:", e)
        return jsonify({"error": str(e)}), 500


# =============================================================================
# MATCH HISTORY ENDPOINTS
# =============================================================================

@app.route('/match_history', methods=['POST'])
def get_match_history():
    """
    Fetch and store match history for a summoner.
    
    Flow:
    1. Get last 20 match IDs from Riot API
    2. For each match:
       a. Check if match exists in our database
       b. If not, fetch match details and store them
       c. Store the player's participation stats
    3. Return summary
    
    This is the "heavy lifting" endpoint that populates our database.
    """
    try:
        data = request.get_json()
        print('Received match_history request:', data)
        
        if not all(key in data for key in ['puuid', 'region']):
            return jsonify({"error": "Missing puuid or region"}), 400
        
        puuid = data['puuid']
        region = data['region']
        routing_region = get_routing_region(region)
        
        # Step 1: Get match IDs from Riot API
        match_ids = retrieve_match_history(puuid, routing_region)
        
        if not match_ids:
            return jsonify({"error": "No matches found"}), 404
        
        print(f"Found {len(match_ids)} matches for {puuid}")
        
        # Step 2: Process each match
        processed_count = 0
        for match_id in match_ids:
            success = process_and_store_match(puuid, match_id, routing_region)
            if success:
                processed_count += 1
        
        db.session.commit()
        
        return jsonify({
            'puuid': puuid,
            'matches_found': len(match_ids),
            'matches_processed': processed_count,
            'first_match': match_ids[0] if match_ids else None,
            'last_match': match_ids[-1] if match_ids else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print("Error in match_history:", e)
        return jsonify({'success': False, 'error': str(e)}), 400


def process_and_store_match(puuid, match_id, routing_region):
    """
    Process a single match and store it in the database.
    
    This function handles:
    1. Checking if we already have this player's stats for this match
    2. Creating the match record if it doesn't exist
    3. Creating/updating the participation record
    
    Returns True if successful, False otherwise.
    """
    try:
        # Check if we already have this participation
        existing = MatchParticipant.query.filter_by(
            puuid=puuid,
            match_id=match_id
        ).first()
        
        if existing:
            print(f"Match {match_id} already exists for {puuid}, skipping")
            return True  # Already have it, consider it a success
        
        # Fetch match data from Riot API
        match_data = get_match_data_from_id(match_id, routing_region)
        
        if not match_data or 'info' not in match_data:
            print(f"No data found for match {match_id}")
            return False
        
        info = match_data['info']
        
        # =====================================================================
        # Step 1: Create or get the Match record
        # =====================================================================
        match = Match.query.get(match_id)
        
        if not match:
            match = Match(
                match_id=match_id,
                game_mode=info.get('gameMode'),
                game_type=info.get('gameType'),
                game_duration=info.get('gameDuration'),
                game_creation=info.get('gameCreation'),
                game_version=info.get('gameVersion'),
                queue_id=info.get('queueId')
            )
            db.session.add(match)
            print(f"Created match record: {match_id}")
        
        # =====================================================================
        # Step 2: Find this player's data in the match
        # =====================================================================
        participant_data = None
        for p in info.get('participants', []):
            if p.get('puuid') == puuid:
                participant_data = p
                break
        
        if not participant_data:
            print(f"Player {puuid} not found in match {match_id}")
            return False
        
        # =====================================================================
        # Step 3: Create the MatchParticipant record
        # =====================================================================
        participation = MatchParticipant(
            match_id=match_id,
            puuid=puuid,
            
            # Result
            win=participant_data.get('win'),
            surrender=participant_data.get('gameEndedInSurrender'),
            
            # Champion
            champ_id=participant_data.get('championId'),
            champ_name=participant_data.get('championName'),
            champ_level=participant_data.get('champLevel'),
            
            # Position
            lane=participant_data.get('lane'),
            role=participant_data.get('role'),
            
            # KDA
            kills=participant_data.get('kills', 0),
            deaths=participant_data.get('deaths', 0),
            assists=participant_data.get('assists', 0),
            first_blood=participant_data.get('firstBloodKill', False),
            
            # Economy
            gold_earned=participant_data.get('goldEarned', 0),
            total_minions_killed=participant_data.get('totalMinionsKilled', 0),
            
            # Items
            item0=participant_data.get('item0', 0),
            item1=participant_data.get('item1', 0),
            item2=participant_data.get('item2', 0),
            item3=participant_data.get('item3', 0),
            item4=participant_data.get('item4', 0),
            item5=participant_data.get('item5', 0),
            item6=participant_data.get('item6', 0),
            
            # Damage dealt
            total_damage_dealt_to_champions=participant_data.get('totalDamageDealtToChampions', 0),
            physical_damage_dealt_to_champions=participant_data.get('physicalDamageDealtToChampions', 0),
            magic_damage_dealt_to_champions=participant_data.get('magicDamageDealtToChampions', 0),
            true_damage_dealt_to_champions=participant_data.get('trueDamageDealtToChampions', 0),
            
            # Damage taken
            total_damage_taken=participant_data.get('totalDamageTaken', 0),
            physical_damage_taken=participant_data.get('physicalDamageTaken', 0),
            magic_damage_taken=participant_data.get('magicDamageTaken', 0),
            true_damage_taken=participant_data.get('trueDamageTaken', 0),
            
            # Utility
            total_heal=participant_data.get('totalHeal', 0),
            total_heals_on_teammates=participant_data.get('totalHealsOnTeammates', 0),
            total_damage_shielded_on_teammates=participant_data.get('totalDamageShieldedOnTeammates', 0),
            
            # Vision
            vision_score=participant_data.get('visionScore', 0),
            wards_placed=participant_data.get('wardsPlaced', 0),
            wards_killed=participant_data.get('wardsKilled', 0),
            
            # Objectives
            objectives_stolen=participant_data.get('objectivesStolen', 0),
            early_surrender=participant_data.get('gameEndedInEarlySurrender'),

            game_creation=info.get('gameCreation'),
            summoner_spell_1=participant_data.get('summoner1Id', 0),
            summoner_spell_2=participant_data.get('summoner2Id', 0)
        )
        
        db.session.add(participation)
        print(f"Added participation for {puuid} in {match_id}")
        return True
        
    except Exception as e:
        print(f"Error processing match {match_id}: {e}")
        return False


@app.route('/receive_match_history/<puuid>', methods=['GET'])
def receive_match_history(puuid):
    """
    Get match IDs for a player from our database.
    
    NEW DESIGN: Instead of storing match_id1 through match_id20 in columns,
    we query the match_participants table and return the match IDs.
    """
    try:
        # Query the last 20 matches, ordered by when we stored them
        participations = db.session.query(MatchParticipant)\
        .filter(MatchParticipant.puuid == puuid)\
        .order_by(MatchParticipant.match_id.desc())\
        .all()
        

        if not participations:
            return jsonify({"error": "No match history found for this player"}), 404
        
        # Return in the same format the frontend expects
        # (for backwards compatibility)
        result = {}
        for i, p in enumerate(participations, 1):
            result[f'match_id{i}'] = [p.match_id, p.game_creation]
        
        print(result)
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in receive_match_history: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/receive_match_stats/<puuid>/<match_id>', methods=['GET'])
def receive_match_stats(puuid, match_id):
    """
    Get stats for a specific player in a specific match.
    
    NEW DESIGN: Queries match_participants and joins with matches
    to get both player stats and match metadata.
    """
    try:
        # Get the participation record
        participation = MatchParticipant.query.filter_by(
            puuid=puuid,
            match_id=match_id
        ).first()
        
        if not participation:
            return jsonify({"error": "Match stats not found"}), 404
        
        result = participation.to_dict_with_match()
        if participation.match:
            result['game_duration'] = participation.match.game_duration
            result['queue_id'] = participation.match.queue_id
        
        return jsonify(result), 200

    except Exception as e:
        print(f"Error in receive_match_stats: {e}")
        return jsonify({"error": str(e)}), 500



# =============================================================================
# RUN THE APP
# =============================================================================

if __name__ == '__main__':
    app.run(debug=True)