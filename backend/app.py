import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import SummonerProfile, SummonerStats
from sqlalchemy import text
from extend import db
from flask_cors import CORS 
from riot_calls.main import get_puuid, get_summoner_id_from_puuid, get_summoner_info
from riot_calls.stats import get_match_data_from_id, get_match_history, process_match_json

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
CORS(app, origins=["http://localhost:3000"])

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
        ret_data = {'success': True, 'error': None, 'id': s_dict['id'], 'icon': s_dict['profileIconId'], 'level': s_dict['summonerLevel'], "summonerName": summoner_name, 'tag_line': tag_line}
        #added summonerName at line 112
        # Create a new SummonerProfile
        new_summoner = SummonerProfile(
            summonerID=summoner_name,
            riot_id=s_dict['id'],
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
        summoners = SummonerProfile.query.all()

        for user in summoners:
            if (user.summonerID == summoner_name) and (user.riot_tag == tag_line):
                s_dict = get_summoner_info(user.puuid, user.region)
                ret_data = {'id': s_dict['id'], 'icon': s_dict['profileIconId'], 'level': s_dict['summonerLevel'], "summonerName": summoner_name, 'tag_line': tag_line}
                print(tag_line)
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

        if not all(key in data for key in ['puuid', 'match_id1', 'match_id2', 'match_id3', 'match_id4', 'match_id5', 'match_id6', 'match_id7', 'match_id8', 'match_id9', 'match_id10', 'match_id11','match_id12', 'match_id13', 'match_id14', 'match_id15', 'match_id16', 'match_id17', 'match_id18', 'match_id19', 'match_id20']):
            return jsonify({"error": "Missing data in request!"}), 400
        
        summoner_name = data['summonerID']
        #riot_id = data['riot_id']
        tag_line = data['riot_tag']
        real_puuid = get_puuid(gameName=summoner_name, tagLine = tag_line)
        region = data['region']
        
        if region == 'NA1':
            history = get_match_history(real_puuid)
        
        elif region == 'EUW1' or 'EUNE1':
            history = get_match_history(real_puuid, 'europe')

        elif region ==  'KR' or 'JP1' or 'VN2':
            history = get_match_history(real_puuid, 'asia')

        else:
            history = get_match_history(real_puuid, 'sea')

        new_history = SummonerStats(
            puuid=real_puuid,
            match_id1=history[0],
            match_id2 = history[1],
            match_id3 = history[2],
            match_id4 = history[3],
            match_id5 = history[4],
            match_id6 = history[5],
            match_id7 = history[6],
            match_id8 = history[7],
            match_id9 = history[8],
            match_id10 = history[9],
            match_id11 = history[10],
            match_id12 = history[11],
            match_id13 = history[12],
            match_id14 = history[13],
            match_id15 = history[14],
            match_id16 = history[15],
            match_id17 = history[16],
            match_id18 = history[17],
            match_id19 = history[18],
            match_id20 = history[19]
        )
        db.session.add(new_history)
        db.session.commit()

        ret_data = {'puuid' : real_puuid, 'first match': history[0], 'last match': history[19]}
        print("History added")
        return jsonify(ret_data)
    
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'success': False, "error": f"Failed to add history: {str(e)}"}), 400
        


if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)

