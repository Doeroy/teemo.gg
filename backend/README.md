# Teemo.gg Backend Documentation

## Overview

The Teemo.gg backend is a Flask-based REST API that integrates with the Riot Games API to fetch and store League of Legends player statistics. It provides endpoints for searching summoners, retrieving match history, and accessing detailed match statistics.

## Tech Stack

- **Framework**: Flask 3.1.0
- **Database**: MySQL with SQLAlchemy ORM
- **API Integration**: Riot Games API v4/v5
- **CORS**: Flask-CORS for cross-origin requests
- **Environment Management**: python-dotenv

## Project Structure

```
backend/
├── app.py                      # Main Flask application with API endpoints
├── models.py                   # SQLAlchemy database models
├── config.py                   # Database configuration
├── extend.py                   # SQLAlchemy instance initialization
├── requirements.txt            # Python dependencies
├── riot_calls/                 # Riot API integration modules
│   ├── main.py                # Core functions (PUUID, Summoner ID retrieval)
│   ├── stats.py               # Match history and stats processing
│   └── life_stats.py          # (Additional stats functions)
└── test_*.py                   # Test files
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- MySQL Database
- Riot Games API Key ([Get one here](https://developer.riotgames.com/))

### 2. Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name

# Riot API Configuration
riot_api_key=your_riot_api_key_here
```

### 4. Database Setup

The application uses three main tables:
- `summoner_prof_test1`: Stores summoner profiles
- `match_history`: Stores last 20 match IDs per player
- `match_stats`: Stores detailed statistics for each match

**Note**: Tables will be created automatically when you run the app if they don't exist.

### 5. Run the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

---

## Database Models

### SummonerProfile
Stores basic summoner information.

| Column      | Type          | Description                                    |
|-------------|---------------|------------------------------------------------|
| `summonerID`| String(50)    | **Display name** (e.g., "Faker") ⚠️           |
| `riot_id`   | String(100)   | **Encrypted Summoner ID** from Riot API ⚠️    |
| `riot_tag`  | String(10)    | Tag line (e.g., "NA1", "KR1")                 |
| `puuid`     | String(100)   | Primary Key - Universal unique identifier     |
| `region`    | String(10)    | Server region (e.g., "na1", "euw1")           |

⚠️ **Important Naming Convention Note**: 
- The column named `summonerID` actually stores the **display name** (what Riot calls `gameName`)
- The column named `riot_id` actually stores the **encrypted Summoner ID** (what Riot calls `id`)
- This is backwards from standard Riot API terminology

### SummonerStats
Stores match history (last 20 match IDs).

| Column       | Type          | Description              |
|--------------|---------------|--------------------------|
| `puuid`      | String(100)   | Primary Key              |
| `match_id1`  | String(255)   | Most recent match ID     |
| `match_id2`  | String(255)   | 2nd most recent match    |
| ...          | ...           | ...                      |
| `match_id20` | String(255)   | 20th most recent match   |

### MatchStats
Stores detailed statistics for individual matches.

| Column                            | Type         | Description                          |
|-----------------------------------|--------------|--------------------------------------|
| `puuid`                           | String(100)  | Primary Key (composite)              |
| `match_id`                        | String(255)  | Primary Key (composite)              |
| `game_mode`                       | String(255)  | Game mode (CLASSIC, ARAM, etc.)      |
| `win`                             | Integer      | 1 if won, 0 if lost                  |
| `kills`                           | Integer      | Number of kills                      |
| `deaths`                          | Integer      | Number of deaths                     |
| `assists`                         | Integer      | Number of assists                    |
| `game_duration`                   | Integer      | Game duration in seconds             |
| `champ_id`                        | Integer      | Champion ID                          |
| `champ_name`                      | String(255)  | Champion name                        |
| `champ_lvl`                       | Integer      | Final champion level                 |
| `goldcount`                       | Integer      | Total gold earned                    |
| `item0` - `item6`                 | Integer      | Item IDs (0-6 slots)                 |
| `first_blood`                     | Boolean      | Whether player got first blood       |
| `lane`                            | String(255)  | Lane position                        |
| `magic_dmg_dealt_to_champions`    | Integer      | Magic damage to champions            |
| `magic_dmg_taken`                 | Integer      | Magic damage taken                   |
| `physical_dmg_dealt_to_champions` | Integer      | Physical damage to champions         |
| `physical_dmg_taken`              | Integer      | Physical damage taken                |
| `true_dmg_dealt_to_champions`     | Integer      | True damage to champions             |
| `true_dmg_taken`                  | Integer      | True damage taken                    |
| `total_dmg_dealt_to_champions`    | Integer      | Total damage to champions            |
| `total_damage_taken`              | Integer      | Total damage taken                   |
| `total_teammate_healing`          | Integer      | Healing provided to teammates        |
| `total_teammate_shielding`        | Integer      | Shielding provided to teammates      |
| `total_minions_killed`            | Integer      | Total CS (creep score)               |
| `objectives_stolen`               | Integer      | Objectives stolen (dragons, barons)  |
| `vision_score`                    | Integer      | Vision score                         |
| `wards_placed`                    | Integer      | Wards placed                         |
| `wards_killed`                    | Integer      | Wards destroyed                      |
| `surrender`                       | Boolean      | Whether team surrendered             |

---

## API Endpoints

### 1. Test Database Connection

**GET** `/test_db`

Tests the MySQL database connection.

**Response:**
```json
"Database connected successfully!"
```

---

### 2. Search Summoner

**POST** `/search`

Searches for a summoner using Riot ID and tag, returns PUUID and Summoner ID.

**Request Body:**
```json
{
  "summonerID": "Faker",
  "riot_tag": "KR1",
  "region": "kr"
}
```

**Response:**
```json
{
  "summonerID": "abc123...",
  "riot_id": "Faker",
  "riot_tag": "KR1",
  "puuid": "xyz789...",
  "region": "kr"
}
```

---

### 3. Search and Add Summoner

**POST** `/search_and_add_summoner`

Fetches summoner data from Riot API and stores it in the database.

**Request Body:**
```json
{
  "summonerID": "Faker",
  "riot_id": "",
  "riot_tag": "KR1",
  "puuid": "",
  "region": "kr"
}
```

**Success Response:**
```json
{
  "success": true,
  "error": null,
  "id": "encrypted_summoner_id",
  "icon": 4321,
  "level": 543,
  "summonerName": "Faker",
  "tag_line": "KR1"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "not_found"
}
```

---

### 4. Retrieve Summoner from Database

**GET** `/search_and_send_summoner`

Retrieves summoner information from the database and updates it with current Riot API data.

**Query Parameters:**
- `summonerID`: Display name (e.g., "Faker")
- `riot_tag`: Tag line (e.g., "KR1")

**Example:**
```
GET /search_and_send_summoner?summonerID=Faker&riot_tag=KR1
```

**Response:**
```json
{
  "id": "encrypted_summoner_id",
  "icon": 4321,
  "level": 543,
  "summonerName": "Faker",
  "tag_line": "KR1",
  "puuid": "xyz789..."
}
```

---

### 5. Get All Summoners

**GET** `/summoners`

Fetches all summoners from the database (for testing).

**Response:**
```json
[
  {
    "summonerID": "Faker",
    "riot_id": "encrypted_id",
    "riot_tag": "KR1",
    "puuid": "xyz789...",
    "region": "kr"
  }
]
```

---

### 6. Fetch Match History

**POST** `/match_history`

Fetches the last 20 matches for a summoner and stores detailed stats for each match.

**Request Body:**
```json
{
  "summonerID": "Faker",
  "riot_id": "",
  "riot_tag": "KR1",
  "puuid": "",
  "region": "kr"
}
```

**Response:**
```json
{
  "puuid": "xyz789...",
  "first_match": "KR_123456789",
  "last_match": "KR_987654321"
}
```

**Note**: This endpoint also triggers the storage of detailed match statistics for all 20 matches.

---

### 7. Retrieve Match History

**GET** `/receive_match_history/<puuid>`

Retrieves stored match IDs for a player.

**Example:**
```
GET /receive_match_history/xyz789...
```

**Response:**
```json
{
  "puuid": "xyz789...",
  "match_id1": "NA1_123456789",
  "match_id2": "NA1_123456790",
  ...
  "match_id20": "NA1_123456808"
}
```

---

### 8. Retrieve Match Statistics

**GET** `/receive_match_stats/<puuid>/<match_id>`

Retrieves detailed statistics for a specific match.

**Example:**
```
GET /receive_match_stats/xyz789.../NA1_123456789
```

**Response:**
```json
{
  "puuid": "xyz789...",
  "match_id": "NA1_123456789",
  "game_mode": "CLASSIC",
  "win": 1,
  "kills": 10,
  "deaths": 2,
  "assists": 8,
  "game_duration": 1834,
  "champ_id": 157,
  "champ_name": "Yasuo",
  "champ_lvl": 18,
  "goldcount": 15430,
  "item0": 6672,
  "item1": 3153,
  ...
}
```

---

## Riot API Integration

### Key Functions (riot_calls/main.py)

#### `get_puuid(gameName, tagLine, region='americas')`
Retrieves a player's PUUID using their Riot ID and tag.

**Parameters:**
- `gameName` (str): Display name (e.g., "Faker")
- `tagLine` (str): Tag (e.g., "KR1")
- `region` (str): Routing region (americas, europe, asia)

**Returns:** PUUID string or `0` if not found

**Riot API Endpoint:** `GET /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}`

---

#### `get_summoner_id_from_puuid(puuid, region='na1')`
Fetches the encrypted Summoner ID from a PUUID.

**Parameters:**
- `puuid` (str): Player's PUUID
- `region` (str): Platform region (na1, kr, euw1, etc.)

**Returns:** Encrypted Summoner ID string

**Riot API Endpoint:** `GET /lol/summoner/v4/summoners/by-puuid/{puuid}`

---

#### `get_summoner_info(puuid, region, api)`
Retrieves complete summoner information (icon, level, IDs).

**Parameters:**
- `puuid` (str): Player's PUUID
- `region` (str): Platform region
- `api` (str): Riot API key

**Returns:** JSON with `id`, `accountId`, `puuid`, `profileIconId`, `revisionDate`, `summonerLevel`

**Riot API Endpoint:** `GET /lol/summoner/v4/summoners/by-puuid/{puuid}`

---

### Key Functions (riot_calls/stats.py)

#### `get_match_history(puuid, region='americas', start=0, count=20)`
Fetches match IDs for a player.

**Parameters:**
- `puuid` (str): Player's PUUID
- `region` (str): Routing region
- `start` (int): Starting index (default: 0)
- `count` (int): Number of matches (default: 20)

**Returns:** List of match IDs

**Riot API Endpoint:** `GET /lol/match/v5/matches/by-puuid/{puuid}/ids`

---

#### `get_match_data_from_id(matchId, region)`
Fetches complete match data for a specific match.

**Parameters:**
- `matchId` (str): Match ID
- `region` (str): Routing region

**Returns:** Complete match JSON

**Riot API Endpoint:** `GET /lol/match/v5/matches/{matchId}`

---

#### `process_match_json(match_json, puuid)`
Processes raw match JSON and extracts relevant statistics for a specific player.

**Parameters:**
- `match_json` (dict): Raw match data from Riot API
- `puuid` (str): Player's PUUID to extract stats for

**Returns:** Dictionary with processed match statistics

---

## Region Mapping

### Riot API uses two types of regions:

1. **Routing Regions** (for account/match endpoints):
   - `americas` - North/South America
   - `europe` - Europe, Middle East, Africa
   - `asia` - Asia, Oceania
   - `sea` - Southeast Asia

2. **Platform Regions** (for summoner endpoints):
   - `na1` - North America
   - `euw1` - Europe West
   - `eune1` - Europe Nordic & East
   - `kr` - Korea
   - `jp1` - Japan
   - `vn2` - Vietnam
   - And more...

**Current Implementation:**
```python
# In /match_history endpoint (lines 235-245)
if region == 'NA1':
    routing_region = 'americas'
elif region in ['EUW1', 'EUNE1']:
    routing_region = 'europe'
elif region in ['KR', 'JP1', 'VN2']:
    routing_region = 'asia'
else:
    routing_region = 'sea'
```

---

## Important Notes & Caveats

### 1. Naming Convention Confusion ⚠️

The current database schema has backwards naming:
- `summonerID` column stores the **display name** (should be `game_name`)
- `riot_id` column stores the **encrypted Summoner ID** (should be `summoner_id`)

This can cause confusion when reading the code. Consider renaming in a future migration.

### 2. Region Logic Bug (Line 238)

```python
# CURRENT (INCORRECT):
elif region == 'EUW1' or 'EUNE1':  # Always True!

# SHOULD BE:
elif region in ['EUW1', 'EUNE1']:
```

### 3. Match History Limitations

- Currently hardcoded to fetch exactly 20 matches
- If fewer than 20 matches exist, `history[19]` will throw an IndexError
- No pagination support for fetching older matches

### 4. API Rate Limiting

The Riot API has rate limits:
- **Development API Key**: 20 requests/second, 100 requests/2 minutes
- **Production API Key**: Higher limits (application required)

The current implementation does NOT handle rate limiting. Consider adding:
- Request throttling
- Retry logic with exponential backoff
- Rate limit header parsing

### 5. Error Handling

Some endpoints lack comprehensive error handling:
- Database connection failures
- Riot API errors (404, 429, 500)
- Invalid input validation

### 6. CORS Configuration

Currently allows requests from `http://localhost:5173` (Vite dev server).

For production, update this in `app.py`:
```python
CORS(app, origins=["http://localhost:5173"])  # Development
CORS(app, origins=["https://yourdomain.com"])  # Production
```

---

## Testing

Test files are provided in the backend directory:

- `test_db.py` - Database connection test
- `test_summoner.py` - Summoner search test
- `test_search.py` - Search endpoint test
- `test_history.py` - Match history test
- `test_match_stats.py` - Match stats test
- `test_recieve_match_stats.py` - Match retrieval test
- `test_recieve_mathc_history.py` - History retrieval test
- `test_mysql_connection.py` - MySQL connection test

---

## Future Improvements

1. **Database Migration**: Rename columns to match Riot API terminology
2. **Add Indexes**: On frequently queried columns (`summonerID`, `riot_tag`)
3. **Caching**: Implement Redis caching for frequently accessed data
4. **Rate Limiting**: Add request throttling for Riot API calls
5. **Error Logging**: Implement proper logging with rotation
6. **Input Validation**: Add request validation with Flask-Marshmallow or Pydantic
7. **Pagination**: Support for fetching matches beyond the last 20
8. **WebSockets**: Real-time updates for live match tracking
9. **Authentication**: Add user authentication if planning multi-user support
10. **Docker**: Containerize the application for easier deployment

---

## Troubleshooting

### Database Connection Failed
- Verify MySQL is running
- Check `.env` credentials
- Ensure database exists: `CREATE DATABASE your_database_name;`

### Riot API 403 Forbidden
- Verify API key is valid
- Check if API key has expired
- Ensure you're using the correct region

### Summoner Not Found (404)
- Verify spelling of summoner name and tag
- Check that the summoner exists in the specified region
- Some special characters may need URL encoding

### CORS Errors
- Ensure frontend is running on `http://localhost:5173`
- Check CORS configuration in `app.py` line 24

---

## License

(Add your license information here)

## Contributors

(Add contributor information here)

---

## Contact & Support

For questions or issues, please refer to:
- [Riot Developer Portal](https://developer.riotgames.com/)
- [Riot API Documentation](https://developer.riotgames.com/apis)