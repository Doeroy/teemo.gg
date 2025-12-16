-- =============================================================================
-- MIGRATION: Create Normalized Database Schema for teemo.gg
-- =============================================================================
-- Run this script in MySQL to create the new tables.
-- 
-- IMPORTANT: This creates NEW tables alongside your existing ones.
-- Your old tables (summoner_prof_test1, match_history, match_stats) are untouched.
-- Once you verify everything works, you can drop the old tables.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TABLE 1: summoners
-- -----------------------------------------------------------------------------
-- Stores one row per player. The puuid is the permanent identifier.
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS summoners (
    -- Primary key: Riot's permanent unique identifier
    puuid VARCHAR(100) PRIMARY KEY,
    
    -- Riot account identifiers
    summoner_id VARCHAR(100),                      -- Internal ID (for ranked API calls)
    riot_name VARCHAR(100) NOT NULL,              -- Display name (e.g., "Faker")
    riot_tag VARCHAR(10) NOT NULL,                -- Tagline (e.g., "KR1")
    region VARCHAR(10) NOT NULL,                  -- Server (NA1, EUW1, KR, etc.)
    
    -- Profile display info
    profile_icon_id INT DEFAULT 0,
    summoner_level INT DEFAULT 1,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for common lookups
    INDEX idx_riot_name_tag (riot_name, riot_tag),  -- For searching by name#tag
    INDEX idx_region (region)                        -- For filtering by region
);

-- -----------------------------------------------------------------------------
-- TABLE 2: matches
-- -----------------------------------------------------------------------------
-- Stores match metadata ONCE per game. This data is the same for all 10 players.
-- We don't want to duplicate "game_duration: 1845" ten times.
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS matches (
    -- Primary key: Riot's match identifier (e.g., "NA1_4823761234")
    match_id VARCHAR(50) PRIMARY KEY,
    
    -- Match metadata (applies to all players)
    game_mode VARCHAR(50),                         -- CLASSIC, ARAM, CHERRY, etc.
    game_type VARCHAR(50),                         -- MATCHED_GAME, CUSTOM_GAME, TUTORIAL
    game_duration INT,                             -- Duration in seconds
    game_creation BIGINT,                          -- Unix timestamp (ms) when game started
    game_version VARCHAR(50),                      -- Patch version (e.g., "14.1.1.456")
    queue_id INT,                                  -- Queue type identifier:
                                                   --   420 = Ranked Solo/Duo
                                                   --   440 = Ranked Flex
                                                   --   400 = Normal Draft
                                                   --   450 = ARAM
                                                   --   See: https://static.developer.riotgames.com/docs/lol/queues.json
    
    -- Timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index for sorting by date
    INDEX idx_game_creation (game_creation DESC)
);

-- -----------------------------------------------------------------------------
-- TABLE 3: match_participants
-- -----------------------------------------------------------------------------
-- THE CORE TABLE. Links players to matches and stores their performance.
-- Each row = "What player X did in match Y"
-- 
-- This is a "junction table" connecting summoners and matches (many-to-many).
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS match_participants (
    -- Auto-incrementing primary key
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Foreign keys (links to other tables)
    match_id VARCHAR(50) NOT NULL,
    puuid VARCHAR(100) NOT NULL,
    
    -- Game result
    win BOOLEAN,
    surrender BOOLEAN,
    
    -- Champion
    champ_id INT,
    champ_name VARCHAR(50),
    champ_level INT,
    
    -- Position
    lane VARCHAR(20),                              -- TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    role VARCHAR(20),                              -- SOLO, NONE, CARRY, SUPPORT
    
    -- KDA
    kills INT DEFAULT 0,
    deaths INT DEFAULT 0,
    assists INT DEFAULT 0,
    first_blood BOOLEAN DEFAULT FALSE,
    
    -- Economy
    gold_earned INT DEFAULT 0,
    total_minions_killed INT DEFAULT 0,
    
    -- Items (slots 0-5 are regular items, slot 6 is trinket)
    item0 INT DEFAULT 0,
    item1 INT DEFAULT 0,
    item2 INT DEFAULT 0,
    item3 INT DEFAULT 0,
    item4 INT DEFAULT 0,
    item5 INT DEFAULT 0,
    item6 INT DEFAULT 0,
    
    -- Damage dealt
    total_damage_dealt_to_champions INT DEFAULT 0,
    physical_damage_dealt_to_champions INT DEFAULT 0,
    magic_damage_dealt_to_champions INT DEFAULT 0,
    true_damage_dealt_to_champions INT DEFAULT 0,
    
    -- Damage taken
    total_damage_taken INT DEFAULT 0,
    physical_damage_taken INT DEFAULT 0,
    magic_damage_taken INT DEFAULT 0,
    true_damage_taken INT DEFAULT 0,
    
    -- Utility
    total_heal INT DEFAULT 0,
    total_heals_on_teammates INT DEFAULT 0,
    total_damage_shielded_on_teammates INT DEFAULT 0,
    
    -- Vision
    vision_score INT DEFAULT 0,
    wards_placed INT DEFAULT 0,
    wards_killed INT DEFAULT 0,
    
    -- Objectives
    objectives_stolen INT DEFAULT 0,
    
    -- Timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- ===========================================================================
    -- CONSTRAINTS
    -- ===========================================================================
    
    -- Unique constraint: Can't have duplicate player+match combinations
    UNIQUE KEY uk_match_participant (match_id, puuid),
    
    -- Foreign keys: Ensure data integrity
    -- If you delete a match, delete all its participants
    -- If you delete a summoner, delete all their participations
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (puuid) REFERENCES summoners(puuid) ON DELETE CASCADE,
    
    -- ===========================================================================
    -- INDEXES (Critical for performance!)
    -- ===========================================================================
    -- These make queries MUCH faster. Without indexes, MySQL scans every row.
    
    INDEX idx_puuid (puuid),                       -- Fast lookup by player
    INDEX idx_match_id (match_id),                 -- Fast lookup by match
    INDEX idx_puuid_created (puuid, created_at DESC),  -- Player's recent matches
    INDEX idx_champ (champ_id)                     -- Find all games on a champion
);

-- =============================================================================
-- VERIFICATION QUERIES (run these to check the tables were created)
-- =============================================================================

-- Show all tables
-- SHOW TABLES;

-- Describe table structure
-- DESCRIBE summoners;
-- DESCRIBE matches;
-- DESCRIBE match_participants;

-- =============================================================================
-- EXAMPLE QUERIES (for reference)
-- =============================================================================

-- Get a player's last 20 matches with stats:
-- SELECT mp.*, m.game_mode, m.game_duration, m.game_creation
-- FROM match_participants mp
-- JOIN matches m ON mp.match_id = m.match_id
-- WHERE mp.puuid = 'your-puuid-here'
-- ORDER BY m.game_creation DESC
-- LIMIT 20;

-- Get win rate for a player:
-- SELECT 
--     COUNT(*) as total_games,
--     SUM(win) as wins,
--     ROUND(SUM(win) / COUNT(*) * 100, 1) as win_rate
-- FROM match_participants
-- WHERE puuid = 'your-puuid-here';

-- Get all participants in a match:
-- SELECT mp.*, s.riot_name, s.riot_tag
-- FROM match_participants mp
-- JOIN summoners s ON mp.puuid = s.puuid
-- WHERE mp.match_id = 'NA1_123456789';



