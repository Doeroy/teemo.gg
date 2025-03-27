import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import SummonerProfile
from sqlalchemy import text
from extend import db
from flask_cors import CORS 
from riot_calls.main import get_puuid, get_summoner_id_from_puuid

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
        riot_id = data['riot_id']
        tag_line = data['riot_tag']
        real_puuid = get_puuid(gameName=summoner_name, tagLine = tag_line)
        region = data['region']

        # Create a new SummonerProfile
        new_summoner = SummonerProfile(
            summonerID=summoner_name,
            riot_id=riot_id,
            riot_tag=tag_line,
            puuid=real_puuid,
            region=region
        )

        db.session.add(new_summoner)
        db.session.commit()
        print("Summoner added!")

        return jsonify({
            "message": "Summoner added successfully!",
            "summonerID": summoner_name,
            "riot_id": riot_id,
            "riot_tag": tag_line,
            "puuid": real_puuid,
            "region": region
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({"error": f"Failed to add summoner: {str(e)}"}), 400

'''
@app.route('/search_and_send_summoner', methods=['GET'])
def retrieve_summoner_info():
    try:
        request.args.get('  ')
    expect Exception as e:
'''




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



if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)

