import requests
import json

url = "http://127.0.0.1:5000/add_summoner"
headers = {"Content-Type": "application/json"}
data = {
    "summonerID": "Summoner789",
    "riot_id": "PlayerC",
    "riot_tag": "NA1",
    "puuid": "abcd-1234-2est",
    "region": "NA"
}

response = requests.post(url, headers=headers, json=data)

# Print the status code and response text
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
