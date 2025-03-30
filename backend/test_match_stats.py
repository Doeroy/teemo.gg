from app import app, db
from models import SummonerStats
from riot_calls.stats import get_match_history

# Run inside Flask's application context
with app.app_context():
    try:
        
        history = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30]
        real_puuid = "abcd-1234-efg"

        # Check if the record exists
        existing_history = SummonerStats.query.filter_by(puuid=real_puuid).first()

        if existing_history:
            # Update existing record
            for i in range(20):
                setattr(existing_history, f"match_id{i+1}", history[i])
        else:
            # Create a new record
            new_history = SummonerStats(
                puuid=real_puuid,
                **{f"match_id{i+1}": history[i] for i in range(20)}
            )
            db.session.add(new_history)

        db.session.commit()
        print("Match history updated successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"Failed to update match history: {e}")