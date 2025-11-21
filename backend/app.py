import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import SummonerProfile, SummonerStats, MatchStats
from sqlalchemy import text
from extend import db
from flask_cors import CORS 
from riot_calls.main import get_puuid, get_summoner_id_from_puuid, get_summoner_info
from riot_calls.stats import get_match_data_from_id, retrieve_match_history, process_match_json

"""
React runs on localhost:3000 and Flask runs on localhost:5000 so our browser will block
requests across different origins. Lines "from flask_cors import CORS" 
and CORS(app, origins=["http://localhost:3000"]) tell flask that its okay to accept request from other
origins
"""

# Load environment variables from .env file
load_dotenv()
print(" DB_HOST =", os.getenv("DB_HOST"))
# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Set up the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)


# Route to test database connection
@app.route('/test_db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return "Database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    summoner_name = data['summonerID']
    tag_line = data['riot_tag']
    region = data['region']
    print(summoner_name, tag_line)
    puuid = get_puuid(gameName=summoner_name, tagLine=tag_line)
    print(puuid)
    return jsonify({'summonerID': get_summoner_id_from_puuid(puuid),
            'riot_id': summoner_name,
            'riot_tag': tag_line,
            'puuid': puuid,
            'region': region
        })

# Route to add a summoner profile (generalized)
@app.route('/add_summoner', methods=['POST'])
def add_summoner():
    try:
        data = request.get_json()  # Get the data from the request body
        # Ensure that the required fields are present
        if not all(key in data for key in ['summonerID', 'riot_id', 'riot_tag', 'puuid', 'region']):
            return jsonify({"error": "Missing data in request!"}), 400

        # Assuming your SummonerProfile model is set up correctly
        new_summoner = SummonerProfile(
            summonerID=data['summonerID'],
            riot_id=data['riot_id'],
            riot_tag=data['riot_tag'],
            puuid=data['puuid'],
            region=data['region']
        )

        db.session.add(new_summoner)
        db.session.commit()

        return jsonify({"message": "Summoner added successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add summoner: {str(e)}"}), 400
    
#route to add a summoner into the database
@app.route('/search_and_add_summoner', methods=['POST'])
def search_and_add_summoner():
    try:
        data = request.get_json()
        print("Incoming data:", data)
        print("Keys present:", list(data.keys()))
        # Validate required fields
        if not all(key in data for key in ['summonerID', 'riot_id', 'riot_tag', 'puuid', 'region']):
            return jsonify({"error": "Missing data in request!"}), 400
        summoner_name = data['summonerID']
        #riot_id = data['riot_id']
        tag_line = data['riot_tag']
        real_puuid = get_puuid(gameName=summoner_name, tagLine = tag_line)
        region = data['region']
        if real_puuid == 0:
            print('reached  it')
            return jsonify({'success': False, 'error': 'not_found' }), 404
        print(real_puuid)

        print(F"PUUID: {real_puuid}")
        s_dict = get_summoner_info(real_puuid, region)
        
        # Handle potential missing fields from Riot API response
        if 'status' in s_dict:
            return jsonify({'success': False, 'error': f"Riot API error: {s_dict.get('message', 'Unknown error')}"}), 400
            
        # Get summoner ID (fallback if missing from response)
        summoner_id = s_dict.get('id')
        if not summoner_id:
            # Try to get summoner ID using the legacy method as fallback
            summoner_id = get_summoner_id_from_puuid(real_puuid, region)
            if not summoner_id:
                summoner_id = "unknown"  # Fallback value
        
        ret_data = {
            'success': True, 
            'error': None, 
            'id': summoner_id, 
            'icon': s_dict.get('profileIconId', 0), 
            'level': s_dict.get('summonerLevel', 1), 
            "summonerName": summoner_name, 
            'tag_line': tag_line
        }
        #added summonerName at line 112
        # Create a new SummonerProfile
        new_summoner = SummonerProfile(
            summonerID=summoner_name,
            riot_id=summoner_id,
            riot_tag=tag_line,
            puuid=real_puuid,
            region=region
        )

        db.session.add(new_summoner)
        db.session.commit()
        print("Summoner added!")
        return jsonify(ret_data)
        '''
        return jsonify({
            "message": "Summoner added successfully!",
            "summonerID": summoner_name,
            "riot_id": s_dict['id'],
            "riot_tag": tag_line,
            "puuid": real_puuid,
            "region": region
        }), 200
        '''
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'success': False, "error": f"Failed to add summoner: {str(e)}"}), 400

#route to search for a specific summoner from the database
@app.route('/search_and_send_summoner', methods=['GET'])
def retrieve_summoner_info():
    try:
        summoner_name = request.args.get('summonerID')
        tag_line = request.args.get('riot_tag')
        print('From /search_and_send_summoner. Summoner_name: ', summoner_name)
        summoners = SummonerProfile.query.all()
        for user in summoners:
            if (user.summonerID == summoner_name) and (user.riot_tag == tag_line):
                s_dict = get_summoner_info(user.puuid, user.region)
                print('From /search_and_send_summoner. s_dict: ', s_dict)
                # Handle potential missing fields from Riot API response (same fix as add endpoint)
                if 'status' in s_dict:
                    return jsonify({"error": f"Riot API error: {s_dict.get('message', 'Unknown error')}"}), 400
                    
                # Get summoner ID (fallback if missing from response)
                summoner_id = s_dict.get('id')
                if not summoner_id:
                    # Try to get summoner ID using the legacy method as fallback
                    summoner_id = get_summoner_id_from_puuid(user.puuid, user.region)
                    if not summoner_id:
                        summoner_id = "unknown"  # Fallback value
                
                ret_data = {
                    'id': summoner_id, 
                    'icon': s_dict.get('profileIconId', 0), 
                    'level': s_dict.get('summonerLevel', 1), 
                    "summonerName": summoner_name, 
                    'tag_line': tag_line,
                    'puuid': s_dict.get('puuid'),
                    'region': user.region,
                }
                return jsonify(ret_data), 200
        return jsonify({"message": "Could not find summoner in database"}), 404
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Failed to retrieve summoner: {str(e)}"}), 400



# Route to fetch all summoners (just for testing)
@app.route('/summoners', methods=['GET'])
def get_summoners():
    try:
        summoners = SummonerProfile.query.all()  # Fetch all summoners from the database
        print("Retrieved summoners:", summoners)
        return jsonify([summoner.to_dict() for summoner in summoners])  # Convert each to dict and return as JSON
    except Exception as e:
        print("/summoners error:", e)
        return jsonify({"error": str(e)}), 500  # Return the error message if something goes wrong
    

@app.route('/match_history', methods=['POST'])
def get_match_history():
    try:
        data = request.get_json()
        print('Data: ', data)
        if not all(key in data for key in ['puuid', 'region']):
            return jsonify({"error": "Missing data in request!"}), 400
        real_puuid = data['puuid']
        region = data['region']
        
        if region == 'NA1':
            history = retrieve_match_history(real_puuid)
        
        elif region == 'EUW1' or 'EUNE1':
            history = retrieve_match_history(real_puuid, 'europe')

        elif region ==  'KR' or 'JP1' or 'VN2':
            history = retrieve_match_history(real_puuid, 'asia')

        else:
            history = retrieve_match_history(real_puuid, 'sea')

        # Build the match_id dictionary
        match_ids = {f"match_id{i+1}": history[i] for i in range(20)}
        
        # Use INSERT ... ON DUPLICATE KEY UPDATE to handle existing records
        columns = ', '.join(['puuid'] + list(match_ids.keys()))
        placeholders = ', '.join([':puuid'] + [f':{key}' for key in match_ids.keys()])
        updates = ', '.join([f'{key} = VALUES({key})' for key in match_ids.keys()])
        
        sql = text(f"""
            INSERT INTO match_history ({columns})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {updates}
        """)
        
        db.session.execute(sql, {'puuid': real_puuid, **match_ids})
        db.session.commit()

        for match_id in history:
            process_match_stats(real_puuid, match_id)

        ret_data = {'puuid': real_puuid, 'first_match': history[0], 'last_match': history[19]}
        print("Match history and stats added.")
        return jsonify(ret_data), 201

        #ret_data = {'puuid' : real_puuid, 'first match': history[0], 'last match': history[19]}
        #print("History added")
        #return jsonify(ret_data)
    
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'success': False, "error": f"Failed to add history: {str(e)}"}), 400


@app.route('/receive_match_history/<puuid>', methods=['GET'])
def receive_match_history(puuid):
    #THIS GETS THE MATCH ID"S OF THE LAST 20 MATCH
    print('This is the PUUID in receive_match_history: ', puuid)
    try:
        user_history = SummonerStats.query.get(puuid)
        if user_history:
            return jsonify(user_history.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
        
    except Exception as e:
        return jsonify({"error in pulling user match history from database": str(e)}), 500


@app.route('/receive_match_stats/<puuid>/<match_id>', methods=['GET'])
def receive_match_stats(puuid, match_id):
    #THIS ONLY GETS THE STATS OF SINGLE MATCH
    try:
        user_history = MatchStats.query.filter_by(puuid=puuid, match_id=match_id).first()

        if user_history:
            return jsonify(user_history.to_dict()), 200
        else:
            return jsonify({"error": "User or match not found"}), 404
        
        
    except Exception as e:
        return jsonify({"error": f"Error in pulling user match history from database: {str(e)}"}), 500

    


#HELPER FUNCTIONS----------------------------------------------------------------------------------------------

def process_match_stats(puuid, match_id):
    """Checks if match stats exist for match_id. If not, fetches and inserts them."""
    
    
    try:
        with db.session.no_autoflush:  # Prevent SQLAlchemy from flushing prematurely
            existing_entry = MatchStats.query.filter_by(puuid=puuid, match_id=match_id).first()

            if existing_entry:
                print(f"Skipping match {match_id} - already exists. Updating instead.")
                match_data = get_match_data_from_id(match_id, 'americas')  # Adjust for region
                if not match_data:
                    print(f"Skipping match {match_id} - no stats found.")
                    return
                
                # Process match data
                match_stats = process_match_json(match_data, puuid)

                # Update existing entry instead of inserting a duplicate
                for key, value in match_stats.items():
                    setattr(existing_entry, key, value)

            else:
                # Fetch match data using Riot API function (get match data by match_id)
                match_data = get_match_data_from_id(match_id, 'americas')  # Adjust for region
                
                if not match_data:
                    print(f"Skipping match {match_id} - no stats found.")
                    return

                # Process match data
                match_stats = process_match_json(match_data, puuid)

                # Insert new match stats
                new_match_stat = MatchStats(puuid=puuid, match_id=match_id, **match_stats)
                db.session.add(new_match_stat)

        db.session.commit()  # Commit only once at the end
        print(f"Match stats processed for {match_id}.")

    except Exception as e:
        db.session.rollback()
        print(f"Error processing match {match_id}: {str(e)}")

    


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)

