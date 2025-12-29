import React, { useState, useEffect} from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { getMainPlatform } from "../../utils/nameValidation";
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


function ChampIconAndLvl({ champName, level }) {
  (champName == 'FiddleSticks') ? champName = 'Fiddlesticks' : champName
  const championIcon = `https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/champion/${champName}.png`;
  return (
    <div className="relative">
      <img
        src={championIcon}
        alt="Champion Icon"
        className="w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-lg sm:rounded-xl"
      />
      <div className="absolute -bottom-1 -right-1 bg-gray-900/90 rounded px-1 py-0.5 text-[10px] sm:text-xs font-bold text-white">
        {level}
      </div>
    </div>
  );
}

function SummonerSpells({icon}){
  const spellIcon = `https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/spell/${SUMMONER_SPELLS[`${icon}_img`]}`
  return(
    <div className="group relative z-50">
      <img 
        src={spellIcon}
        alt="Summoner spell image"
        className="w-5 h-5 sm:w-6 sm:h-6 md:w-7 md:h-7 rounded"
      />
      <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 
                   bg-gray-900/95 backdrop-blur-md text-white text-sm rounded-lg 
                   opacity-0 invisible group-hover:opacity-100 group-hover:visible 
                   transition-all duration-200 whitespace-nowrap pointer-events-none
                   border border-white/10 shadow-xl z-[100] max-w-xs
                   after:content-[''] after:absolute after:top-full after:left-1/2 
                   after:-translate-x-1/2 after:border-4 after:border-transparent 
                   after:border-t-gray-900/95">
          <span className="text-amber-400 font-semibold">
            {`${SUMMONER_SPELLS[icon]}: `}
          </span>
          <span className="text-gray-200 whitespace-normal">
            {SUMMONER_SPELLS[`${icon}_description`]}
          </span>
      </span>
    </div>
  )
}
function ItemGrid({ data }) {
  return (
    <div className="flex gap-0.5 sm:gap-1">
      {/* All 7 items in one row */}
      {[0, 1, 2, 3, 4, 5, 6].map((i) => (
        <div key={i}>
          {data && data[`item${i}`] !== 0 ? (
            <img
              src={`https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/item/${data[`item${i}`]}.png`}
              alt={`item ${i}`}
              className={`w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 ${i === 6 ? 'rounded-full' : 'rounded-md'}`}
            />
          ) : (
            <div className={`w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 bg-black/40 ${i === 6 ? 'rounded-full' : 'rounded-md'}`} />
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
    <div className="flex flex-col justify-center items-start min-w-[70px] sm:min-w-[90px] pr-2 sm:pr-4">
      <p className="text-[10px] sm:text-xs text-white/50 font-medium whitespace-nowrap">
        {QUEUE_NAMES[data.queue_id] || 'Game'}
      </p>
      <p className={`text-sm sm:text-base font-bold ${data.win ? 'text-cyan-400' : 'text-rose-400'}`}>
        {data.win ? 'Victory' : 'Defeat'}
      </p>
      <p className="text-xs text-white/50">
        {`${timeMinutes}:${timeSeconds.toString().padStart(2, '0')}`}
      </p>
    </div>
  )
}
function Team({team, isBlueTeam}) {
  return (
    <div className="flex flex-col gap-0.5">
      {team && team.map((member, index) => 
      {
        const championName = (member.champ_name == 'FiddleSticks') ? 'Fiddlesticks' : member.champ_name
        const encodedName = encodeURIComponent(`${member.summoner_name}#${member.summoner_tag}`)
        return(
          <div className="flex items-center gap-1" key={member.puuid || index}>
            <img
              src={`https://ddragon.leagueoflegends.com/cdn/${VERSION}/img/champion/${championName}.png`}
              alt={championName}
              className="w-4 h-4 rounded-sm"
            />
            <Link 
              to={`/summoners/${getMainPlatform(member.summoner_region)}/${encodedName}`} 
              reloadDocument={true}
              className={`text-[10px] lg:text-xs truncate max-w-[50px] lg:max-w-[70px] hover:underline ${
                isBlueTeam ? 'text-white/60 hover:text-white/90' : 'text-white/60 hover:text-white/90'
              }`}
            >
              {member.summoner_name}
            </Link>
          </div>
        )
      })}
    </div>
  );
}

function Kda({ stats }) {
  const csScore = stats.total_minions_killed / (stats.game_duration / 60);
  const kda = stats.deaths === 0 ? 'Perfect' : ((stats.kills + stats.assists) / stats.deaths).toFixed(2);
  const kdaValue = stats.deaths === 0 ? Infinity : (stats.kills + stats.assists) / stats.deaths;
  
  // Color based on KDA performance
  const kdaColor = kdaValue >= 5 ? 'text-amber-400' : kdaValue >= 3 ? 'text-cyan-400' : 'text-white/80';
  
  return (
    <div className="flex flex-col justify-center px-2 sm:px-4 min-w-[80px] sm:min-w-[100px]">
      <p className="text-base sm:text-lg font-bold tracking-wide">
        <span className="text-white">{stats.kills}</span>
        <span className="text-white/40"> / </span>
        <span className="text-rose-400">{stats.deaths}</span>
        <span className="text-white/40"> / </span>
        <span className="text-white">{stats.assists}</span>
      </p>
      <p className={`text-xs sm:text-sm font-semibold ${kdaColor}`}>
        {kda} KDA
      </p>
      <p className="text-xs text-white/50 mt-0.5 hidden sm:block">
        {stats.total_minions_killed} CS ({csScore.toFixed(1)}/m)
      </p>
    </div>
  );
}

function DamageVision({ stats }) {
  // Format damage to K notation
  const formatDamage = (dmg) => {
    if (dmg >= 1000) return (dmg / 1000).toFixed(1) + 'k';
    return dmg;
  };
  
  // Estimate max damage for bar (rough estimate based on typical game values)
  const maxDamage = 50000;
  const maxVision = 50;
  
  const damagePercent = Math.min((stats.total_damage_dealt_to_champions / maxDamage) * 100, 100);
  const visionPercent = Math.min((stats.vision_score / maxVision) * 100, 100);
  
  return (
    <div className="hidden md:flex flex-col justify-center gap-1.5 min-w-[100px] px-2">
      {/* Damage Bar */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 w-14">Damage</span>
        <div className="flex-1 h-2 bg-black/30 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-orange-500 to-red-500 rounded-full"
            style={{ width: `${damagePercent}%` }}
          />
        </div>
        <span className="text-xs text-white/70 w-10 text-right">{formatDamage(stats.total_damage_dealt_to_champions)}</span>
      </div>
      {/* Vision Bar */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 w-14">Vision</span>
        <div className="flex-1 h-2 bg-black/30 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
            style={{ width: `${visionPercent}%` }}
          />
        </div>
        <span className="text-xs text-white/70 w-10 text-right">{stats.vision_score}</span>
      </div>
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
        setStats(response.data);
      } catch (error) {
        console.log("Error fetching users champ:", error);
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
      <div className="mb-2 rounded-lg bg-slate-800/60 p-3 animate-pulse">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-slate-700/50 rounded-lg"></div>
          <div className="flex-1 space-y-2">
            <div className="h-3 bg-slate-700/50 rounded w-1/4"></div>
            <div className="h-2 bg-slate-700/50 rounded w-1/3"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  // Subtle slate gradient with colored left border like the mockup
  const borderColor = stats.win ? 'border-l-cyan-400' : 'border-l-rose-500';

  return (
    <div className={`
      mb-2 rounded-lg 
      bg-gradient-to-r from-slate-800/90 via-slate-800/70 to-slate-700/50
      border-l-4 ${borderColor}
      backdrop-blur-sm
      transition-all duration-200 hover:brightness-110
      text-white
    `}>
      <div className="flex items-center p-2 sm:p-3 gap-1 sm:gap-2 md:gap-3">
        {/* Match Info */}
        <MatchInfo data={stats}/>
        
        {/* Champion + Spells */}
        <div className="flex items-center gap-1 sm:gap-2">
          <ChampIconAndLvl champName={stats.champ_name} level={stats.champ_level} />
          <div className="flex flex-col gap-0.5">
            <SummonerSpells icon={stats.summoner_spell_1}/>
            <SummonerSpells icon={stats.summoner_spell_2}/>
          </div>
        </div>
        
        {/* KDA */}
        <Kda stats={stats} />
        
        {/* Damage/Vision Bars - hidden on mobile */}
        <DamageVision stats={stats} />
        
        {/* Items */}
        <div className="px-1 sm:px-3">
          <ItemGrid data={stats} />
        </div>
        
        {/* Teams - hidden on small screens */}
        <div className="hidden lg:flex gap-3 ml-auto pl-3 border-l border-white/10">
          <Team team={stats.blue_team} isBlueTeam={true}/>
          <Team team={stats.red_team} isBlueTeam={false}/>
        </div>
      </div>
    </div>
  );
}

export default function SummonerCard({ data }) {
  if (!data) return null;
  const [matches, setMatches] = useState();
  
  useEffect(() => {
    const getMatches = async () => {
      try {
        const post_response = await axios.post(
          `http://localhost:5000/match_history`,
          { puuid: data.puuid, region: data.region }
        );

        const get_response = await axios.get(
          `http://localhost:5000/receive_match_history/${data.puuid}`
        );

        setMatches(get_response.data);
      } catch (error) {
        console.log("Error fetching users data:", error);
      }
    };
    getMatches();
  }, [data.puuid, data.region]);

  if (!data || !data.summonerName || !data.icon) {
    return null;
  }

  return (
    <div className="w-full max-w-5xl px-2 sm:px-0">
      {/* Header */}
      <div className="flex items-center justify-between mb-3 sm:mb-4">
        <h2 className="text-lg sm:text-xl font-bold text-white/90 flex items-center gap-2">
          Match History
        </h2>
        <span className="text-xs sm:text-sm text-white/50">
          {matches ? Object.keys(matches).length : 0} games
        </span>
      </div>
      
      {/* Match List */}
      <div>
        {matches &&
          Object.values(matches).sort((matchA, matchB) => matchB[1] - matchA[1]).map((match) => (
            <MatchesSection matchId={match[0]} puuid={data.puuid} key={match[0]}/>
          ))}
      </div>
    </div>
  );
}