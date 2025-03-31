from app import app, db
from models import SummonerStats
from riot_calls.stats import get_match_history

# Run inside Flask's application context
with app.app_context():
    try:
        
        real_puuid = "50nE-TyXu7VHhzSfaGDyzl1aJeJ2NMySrhPq-hrSmGhTAvd4HZibMbeIZ9eqi2Q93yrOGM14w9_BaQ"
        history = get_match_history(real_puuid)
        region = "americas"


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