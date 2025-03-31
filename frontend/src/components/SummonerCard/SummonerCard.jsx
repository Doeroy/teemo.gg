import React, {useState} from 'react'
import styles from './SummonerCard.module.css'

function KDA(){
    let summonerIcon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg`;
    let championIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/145.png'
    return(
        <div className={styles.container}>
            <div>
                <img src={championIcon} alt='Champion Icon' className={styles.championIcon}></img>
            </div>
            <p>10/<inline className = {styles.deaths}>1</inline>/5</p>
            <div className={styles.allyTeam}>
                <div>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img><inline>Hai</inline>
                </div>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
            </div>
            <div className={styles.allyTeam}>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img>
            </div>
            <div className={styles.enemyTeam}>

            </div>
        </div>
    );
}

export default function SummonerCard({data}){
    if (!data || !data.summonerName || !data.icon) {
        return null; // Render nothing if there's no valid data
    }
    let lvl = data.level;
    let summonerName = data.summonerName
    let icon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${data.icon}.jpg`;
    let tag = data.tag_line
    console.log("tag: ", tag)
  
    
    return(
        <div>   
            <img src={icon} alt="Summoner Icon" id ={styles.summonerIcon}></img>
            <h5>{`${summonerName}#${tag} Level: ${lvl}`}</h5>
            <KDA/>
        </div>
    );
}

