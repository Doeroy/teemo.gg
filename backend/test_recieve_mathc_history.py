from app import app

# Define your real puuid here
real_puuid = "50nE-TyXu7VHhzSfaGDyzl1aJeJ2NMySrhPq-hrSmGhTAvd4HZibMbeIZ9eqi2Q93yrOGM14w9_BaQ"

with app.test_client() as client:
    response = client.get(f'/receive_match_history/{real_puuid}')
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.get_json())