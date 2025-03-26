from app import app, db
from models import SummonerProfile

# Run inside Flask's application context
with app.app_context():
    try:
        new_summoner = db.session

        db.session.add(new_summoner)
        db.session.commit()
        print("Summoner added successfully!")

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print(f"Failed to add summoner: {e}")
