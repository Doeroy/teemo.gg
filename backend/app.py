import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import SummonerProfile
from sqlalchemy import text
from extend import db

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

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
    

# Route to add a summoner profile (generalized)
@app.route('/add_summoner', methods=['POST'])
def add_summoner():
    try:
        data = request.get_json()  # Get the data from the request body
        # Ensure that the required fields are present
        if not all(key in data for key in ['summonerID', 'riot_id', 'riot_tag', 'puuid', 'reigon']):
            return jsonify({"error": "Missing data in request!"}), 400

        # Assuming your SummonerProfile model is set up correctly
        new_summoner = SummonerProfile(
            summonerID=data['summonerID'],
            riot_id=data['riot_id'],
            riot_tag=data['riot_tag'],
            puuid=data['puuid'],
            reigon=data['reigon']
        )

        db.session.add(new_summoner)
        db.session.commit()

        return jsonify({"message": "Summoner added successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add summoner: {str(e)}"}), 400


# Route to fetch all summoners (just for testing)
@app.route('/summoners', methods=['GET'])
def get_summoners():
    try:
        summoners = SummonerProfile.query.all()  # Fetch all summoners from the database
        return jsonify([summoner.to_dict() for summoner in summoners])  # Convert each to dict and return as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return the error message if something goes wrong



if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)

