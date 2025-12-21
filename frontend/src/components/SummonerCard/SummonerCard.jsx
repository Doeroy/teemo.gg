import React, { useState, useEffect, use } from "react";
import axios from "axios";

const VERSION = "15.24.1";

const SUMMONER_SPELLS = {}

const getSpell = async () => {
  const get_sums = await axios.get(`https://ddragon.leagueoflegends.com/cdn/${VERSION}/data/en_US/summoner.json`);
  Object.values(get_sums.data.data).forEach((spell) => {
      SUMMONER_SPELLS[spell.key] = spell.name;
      SUMMONER_SPELLS[`${spell.key}_description`] = spell.description;
      SUMMONER_SPELLS[`${spell.key}_img`] = spell.image.full
  })
}
getSpell();

const QUEUE_NAMES = {
  420: "Ranked Solo/Duo",
  440: "Ranked Flex",
  400: "Normal Draft",
  430: "Normal Blind",
  450: "ARAM",
  490: "Quickplay",
  700: "Clash",
  900: "URF",
  1700: "Arena",
};

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
  const championIcon = `https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/champion/${champName}.png`;
  return (
    <div className="relative">
      <img
        src={championIcon}
        alt="Champion Icon"
        className="w-13 sm:w-14 md:w-16 lg:w-18 rounded-2xl"
      />
      <div className="absolute bottom-0 bg-black rounded-lg w-5 text-sm text-white text-center">
        {level}
      </div>
    </div>
  );
}

function SummonerSpells({icon}){
  const spellIcon = `https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/spell/${SUMMONER_SPELLS[`${icon}_img`]}`
  console.log('HERE ICON: ', SUMMONER_SPELLS[icon])
  return(
    <div className="group relative">
      <img 
        src={spellIcon}
        alt="Summoner spell image"
        className="h-8 rounded-md"
      />
      <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 
                   bg-gray-900 text-white text-sm rounded 
                   opacity-0 invisible group-hover:opacity-100 group-hover:visible 
                   transition-opacity duration-200 whitespace-nowrap pointer-events-none
                   after:content-[''] after:absolute after:top-full after:left-1/2 
                   after:-translate-x-1/2 after:border-4 after:border-transparent 
                   after:border-t-gray-900">
          <span className="text-yellow-300">
            {`${SUMMONER_SPELLS[icon]}: `}
          </span>
          {SUMMONER_SPELLS[`${icon}_description`]}
      </span>
    </div>
    
  )
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

function MatchInfo({data}){
  const timeMinutes = Math.floor(data.game_duration / 60)
  const timeSeconds = (data.game_duration % 60)

  return(
    <div>
      <p>{QUEUE_NAMES[data.queue_id]}</p>
      <hr></hr>
      <p>{`${timeMinutes}:${timeSeconds.toString().padStart(2, '0')}`}</p>
      <p>{data.win ? 'Victory' : 'Defeat'}</p>
    </div>
  )
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
        <span className="font-bold">
          {stats.kills}
        </span> 
        / 
        <span className="font-bold text-red-500">
          {stats.deaths}
        </span> 
        / 
        <span className="font-bold">
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
        Vision: {stats.vision_score}
      </p>
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
    <div className={stats.win ? 'bg-blue-400 m-4 flex rounded-lg p-2' : 'bg-red-400 m-4 flex rounded-lg p-2'}>
      <div className="flex">
        <MatchInfo data={stats}/>
        <div>
          <ChampIconAndLvl champName={stats.champ_name} level={stats.champ_level} />
        </div>
        <div className="m-1">
          <SummonerSpells icon={stats.summoner_spell_1}/>
          <SummonerSpells icon={stats.summoner_spell_2}/>
        </div>
      </div>
      <Kda stats={stats} />
      <ItemGrid data={stats} />
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
        Object.values(matches).sort((matchA, matchB) => matchB[1] - matchA).map((match) => (
          <MatchesSection matchId={match[0]} puuid={data.puuid} key={match}/>
        ))}
    </div>
  );
}