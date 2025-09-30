import React, {useState} from 'react'
import styles from './SummonerCard.module.css'

function SummonerInfo({data}){
    let lvl = data.level;
    let summonerName = data.summonerName
    let icon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${data.icon}.jpg`;
    let tag = data.tag_line
    console.log("tag: ", tag)

    return(
        <div>   
            <img src={icon} alt="Summoner Icon" id ={styles.summonerIcon}></img>
            <h5>{`${summonerName}#${tag} Level: ${lvl}`}</h5>
        </div>
    );
}

function ChampIconAndLvl(){
    let championIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/145.png';

    return(
        <div className={styles.championIconContainer}>
                <img src={championIcon} alt='Champion Icon' className={styles.championIcon}></img>
            <div className={styles.champAndLvl}>
                18
            </div>
        </div>
    );
}

function ItemGrid(){
    return(
    <div className={styles.itemsGrid}>
        <div className={styles.items}></div>
        <div className={styles.items}></div>
        <div className={styles.items}></div>
        <div className={styles.items}></div>
        <div className={styles.items}></div>
        <div className={styles.items}></div>
        <div className={styles.items}></div>
    </div>
    );
}

function AllyTeam(){
    let summonerIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg';
    return(
        <div className={styles.allyTeam}>
            <div>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img><span>Hai</span>
            </div>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
        </div>
    );
}

function EnemyTeam(){
    let summonerIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg';
    return(
    <div className={styles.enemyTeam}>
        <div>
            <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img><span>Daniel</span>
        </div>
        <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
        <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
        <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
        <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
    </div>
    );
}

function Kda(){
    return(
    <div className={styles.kdaSection}>
        <p className={styles.font}><span className = {styles.kills}>10</span>/<span className = {styles.deaths}>
            1</span>/<span>5</span></p>
        <ItemGrid/>
    </div>
    );
}

export default function SummonerCard({data}){
    if (!data || !data.summonerName || !data.icon) {
        return null; // Render nothing if there's no valid data
    }
    console.log('here: ', data)
    let summonerIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg';
    return(
        <>
            <SummonerInfo data = {data}/>
            <div className = {styles.flex}>
                <div className={styles.cardContainer}>
                    <ChampIconAndLvl/>
                    <Kda/>
                    <AllyTeam/>
                    <EnemyTeam/>
                </div>
            </div>
        </>
    );
}
