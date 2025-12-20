import React, { useState, useEffect, use } from "react";
import axios from "axios";

const VERSION = "15.24.1";
/*
Unused CHAMP_MAPPING
const CHAMP_MAP = {}
function championMap () {
  useEffect(() => {
    const getChampMap = async () => {
      const getChampNames = await axios.get(`https://ddragon.leagueoflegends.com/cdn/${VERSION}/data/en_US/champion.json`);
      Object.values(getChampNames.data.data).forEach((champ) => {
          CHAMP_MAP[champ.key] = champ.id;
      })
    }
    getChampMap()
  }, [])
}
*/

function SummonerInfo({ data }) {
  let lvl = data.level;
  let summonerName = data.summonerName;
  let icon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${data.icon}.jpg`;
  let tag = data.tag_line;
  return (
    <>
      <div className="w-35 max-w-md">
        <div className="relative">
          <img
            src={icon}
            alt="Summoner Icon"
            className="aspect-square w-full object-cover border-3 rounded-lg"
          />
          <p className="absolute bottom-30 left-14 bg-black rounded-lg border-3">
            {lvl}
          </p>
        </div>
      </div>
      <p>
        <span className="font-bold">{`${summonerName} `}</span>
        <span className="text-gray-300 font-medium">{`#${tag}`}</span>
      </p>
    </>
  );
}

function ChampIconAndLvl({ champName, level }) {
  let championIcon = `https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/champion/${champName}.png`;
  return (
    <div className="relative">
      <img
        src={championIcon}
        alt="Champion Icon"
        className="w-13 sm:w-14 md:w-16 lg:w-18 rounded-2xl"
      />
      <div className="absolute bottom-0 bg-black rounded-lg w-5 text-sm">
        {level}
      </div>
    </div>
  );
}

function ItemGrid({ data }) {
  return (
    <div className="grid grid-cols-4 grid-rows-2 gap-1">
      <img
        src={`https://ddragon.leagueoflegends.com/cdn/15.24.1/img/item/${
          data[`item${6}`]
        }.png`}
        alt={`item ${6}`}
        className="col-start-4 col-end-4 row-start-1 row-end-1 h-10 rounded-lg"
      />
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <div key={i}>
          {data && data[`item${i}`] !== 0 ? (
            <img
              src={`https://ddragon.leagueoflegends.com/cdn/15.24.1/img/item/${
                data[`item${i}`]
              }.png`}
              alt={`item ${i}`}
              className="h-10 rounded-lg"
            />
          ) : (
            <div className="h-10 rounded-lg bg-white"> </div>
          )}
        </div>
      ))}
    </div>
  );
}

function Team() {
  let summonerIcon =
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg";
  return (
    <div className={styles.enemyTeam}>
      <div>
        <img
          src={summonerIcon}
          alt="Summoner Icon"
          className={styles.miniIcon}
        ></img>
        <span>Daniel</span>
      </div>
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
    </div>
  );
}

function Kda({ stats }) {
  const csScore = stats.total_minions_killed / (stats.game_duration / 60);
  return (
    <div>
      <p>
        <span>
          {stats.kills}
        </span> 
        / 
        <span className="text-red-500">
          {stats.deaths}
        </span> 
        / 
        <span>
          {stats.assists}
        </span>
      </p>
      <p className="text-sm">
        KDA: {((stats.kills + stats.assists) / stats.deaths).toFixed(2)}
      </p>
      <p className="text-sm">
        CS: {stats.total_minions_killed} ({csScore.toFixed(1)})
      </p>
      <p className="text-sm">
        Vision Score: {stats.vision_score}
      </p>
    </div>
  );
}

export default function SummonerCard({ data }) {
  if (!data) return null;
  const [matches, setMatches] = useState();
  console.log("data: ", data);
  console.log(`data.puuid: ${data.puuid} data.region: ${data.region}`);
  useEffect(() => {
    const getMatches = async () => {
      try {
        const post_response = await axios.post(
          `http://localhost:5000/match_history`,
          { puuid: data.puuid, region: data.region }
        );
        console.log("Post response:", post_response.data);

        const get_response = await axios.get(
          `http://localhost:5000/receive_match_history/${data.puuid}`
        );
        console.log("Get response:", get_response.data);

        setMatches(get_response.data);
        console.log("Match Data: ", get_response.data);
      } catch (error) {
        console.log("Error fetching users data:", error);
      }
    };
    getMatches();
  }, [data.puuid, data.region]);
  if (!data || !data.summonerName || !data.icon) {
    return null; // Render nothing if there's no valid data
  }

  console.log('matches: ', matches)
  return (
    <div className="h-full">
      {matches &&
        Object.values(matches).map((match) => (
          <MatchesSection matchId={match} puuid={data.puuid} />
        ))}
    </div>
  );
}

function MatchesSection({ matchId, puuid }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const getChamp = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/receive_match_stats/${puuid}/${matchId}`
        );
        console.log("HERE : ", response);
        setStats(response.data);
      } catch (error) {
        console.log("Error fetching users champ:", error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    if (matchId && puuid) {
      getChamp();
    }
  }, [matchId, puuid]);

  if (loading) {
    return (
      <div className="h-full bg-slate-900 animate-pulse">
        <div className="w-16 h-16 bg-slate-800 rounded-lg"></div>
      </div>
    );
  }

  if (!stats) {
    return;
  }

  
  return (
    <div className={stats.win ? 'bg-blue-400 m-4' : 'bg-red-400 m-4'}>
      <ChampIconAndLvl champName={stats.champ_name} level={stats.champ_level} />
      <ItemGrid data={stats} />
      <Kda stats={stats} />
    </div>
  );
}
