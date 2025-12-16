from app import app, db
from models import SummonerStats, MatchStats
from riot_calls.stats import get_match_data_from_id, process_match_json, retrieve_match_history

# Run inside Flask's application context
with app.app_context():
    try:
        
        #history = ["match1", "match2", "match3", "match4", "match5", "match6", "match7", "match8", "match9", "match10", "match11", "match12", "match13", "match14", "match15", "match16", "match17", "match18", "match19", "match20"]
        real_puuid = "91nxuarDLMu2vrtqvVZ0Y5UFIE5cemvJyffmKX8KNBJiaRCBziDIcO14mEOqpXnAdGZZm-LQB6v7pA"
        history = retrieve_match_history(real_puuid)
        region = "americas"  # Adjust based on your needs

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

        # Process and add match stats
        for match_id in history:
            match_data = get_match_data_from_id(match_id, region)
            if match_data:
                match_stats = process_match_json(match_data, real_puuid)
                existing_stats = MatchStats.query.filter_by(puuid=real_puuid, match_id=match_id).first()
                
                if existing_stats:
                    # Update existing stats
                    for key, value in match_stats.items():
                        setattr(existing_stats, key, value)
                else:
                    # Insert new stats
                    new_match_stat = MatchStats(puuid=real_puuid, match_id=match_id, **match_stats)
                    db.session.add(new_match_stat)
            
        db.session.commit()
        print("Match stats added successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"Failed to update match history and stats: {e}")