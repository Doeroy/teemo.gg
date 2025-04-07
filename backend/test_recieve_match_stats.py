from app import app

# Define your real puuid here
real_puuid = "91nxuarDLMu2vrtqvVZ0Y5UFIE5cemvJyffmKX8KNBJiaRCBziDIcO14mEOqpXnAdGZZm-LQB6v7pA"
real_match_id = "NA1_5219843212"
with app.test_client() as client:
    response = client.get(f'/receive_match_stats/{real_puuid}/{real_match_id}')
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.get_json())