import React, { useState, useEffect } from "react";
import styles from "./SummonerCard.module.css";
import axios from "axios";

function SummonerInfo({ data }) {
  let lvl = data.level;
  let summonerName = data.summonerName;
  let icon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${data.icon}.jpg`;
  let tag = data.tag_line;
  return (
    <div>
      <img src={icon} alt="Summoner Icon" id={styles.summonerIcon}></img>
      <h5>{`${summonerName}#${tag} Level: ${lvl}`}</h5>
    </div>
  );
}

function ChampIconAndLvl({ matchId, puuid }) {
  const [champId, setChampId] = useState("");
  const [lvl, setLvl] = useState("");
  useEffect(() => {
    const getChamp = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/receive_match_stats/${puuid}/${matchId}`
        );
        setChampId(response.data.champ_id);
        setLvl(response.data.champ_lvl);
      } catch (error) {
        console.log("Error fetching users champ:", error);
      }
    };
    if (matchId) {
      getChamp();
    }
  }, [matchId, puuid]);
  console.log("champId: ", champId);
  let championIcon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${champId}.png`;
  return (
    <div className={styles.championIconContainer}>
      <img
        src={championIcon}
        alt="Champion Icon"
        className={styles.championIcon}
      ></img>
      <div className={styles.champAndLvl}>{lvl}</div>
    </div>
  );
}

function ItemGrid({matchId, puuid}) {
  const [items, setItems] = useState();
  console.log('item grid: ', matchId)
  useEffect(() => {
    const getItems = async () => {
      try{
        const response = await axios.get(`http://localhost:5000/receive_match_stats/${puuid}/${matchId}`); //this await makes it so the async function has to wait on the promise from this function to resolve. usually this would return a promise and resolve later15
        setItems(response.data);
      }catch(err) {
        console.log(err);
      }
    }
    getItems();
  }, [puuid, matchId]);

  return (
    <div className={styles.itemsGrid}>
      {[0, 1, 2, 3, 4, 5, 6].map((i) => (
        <div key={i} className={styles.items}>
          {items && items[`item${i}`] !== 0 && (
            <img
              src={`https://ddragon.leagueoflegends.com/cdn/15.24.1/img/item/${items[`item${i}`]}.png`}
              alt={`item ${i}`}
            />
          )}
        </div>
      ))}
    </div>
  );
}

function AllyTeam() {
  let summonerIcon =
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg";
  return (
    <div className={styles.allyTeam}>
      <div>
        <img
          src={summonerIcon}
          alt="Summoner Icon"
          className={styles.miniIcon}
        ></img>
        <span>Hai</span>
      </div>
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
      <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon} />
    </div>
  );
}

function EnemyTeam() {
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

function Kda({ matchId, puuid }) {
  const [kda, setKda] = useState("");
  useEffect(() => {
    const getKda = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/receive_match_stats/${puuid}/${matchId}`
        );
        console.log("KDA: ", response.data);
        setKda(response.data);
      } catch (error) {
        console.log("Error fetching users kda:", error);
      }
    };
    if (matchId) {
      getKda();
    }
  }, [matchId, puuid]);
  console.log(kda);
  const csScore = kda.total_minions_killed / (kda.game_duration / 60);
  return (
    <div className={styles.kdaSection}>
      <p className={styles.font}>
        <span className={styles.kills}>{kda.kills}</span>/
        <span className={styles.deaths}>{kda.deaths}</span>/
        <span>{kda.assists}</span>
      </p>
      <p className="text-sm">
        KDA: {((kda.kills + kda.assists) / kda.deaths).toFixed(2)}
      </p>
      <p className="text-sm">
        CS: {kda.total_minions_killed} ({csScore.toFixed(1)})
      </p>
      <p className="text-sm">Vision Score: {kda.vision_score}</p>
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
        // First, post to fetch and store match history
        const post_response = await axios.post(
          `http://localhost:5000/match_history`,
          { puuid: data.puuid, region: data.region }
        );
        console.log("Post response:", post_response.data);

        // Then, get the stored match history
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

  if (matches){
    Object.values(matches).map((match) => {
      console.log(match)
    })
  }
  return (
    <>
    <SummonerInfo data={data} />
    {matches && Object.values(matches).map((match) => 
      <div className={styles.flex} key={match}>
        <div className={styles.cardContainer}>
          <ChampIconAndLvl matchId={match} puuid={data.puuid} />
          <div>
            <Kda matchId={match} puuid={data.puuid} />
            <ItemGrid matchId={match} puuid={data.puuid} />
          </div>
          <AllyTeam />
          <EnemyTeam />
        </div>
      </div>
    )}
    </>
  );
}
