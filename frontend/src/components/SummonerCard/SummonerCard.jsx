import React, {useState} from 'react'
import styles from './SummonerCard.module.css'

function KDA(){
    let summonerIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/3150.jpg';
    let championIcon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/145.png';
    return(
        <div className = {styles.flex}>
            <div className={styles.cardContainer}>
                <div className={styles.championIconContainer}>
                    <img src={championIcon} alt='Champion Icon' className={styles.championIcon}></img>
                    <div className={styles.champAndLvl}>18</div>
                </div>

                <div className={styles.kdaSection}>
                    <p className={styles.font}><span className = {styles.kills}>10</span>/<span className = {styles.deaths}>
                        1</span>/<span>5</span></p>
                        <div className={styles.itemsGrid}>
                            <div className={styles.items}></div>
                            <div className={styles.items}></div>
                            <div className={styles.items}></div>
                            <div className={styles.items}></div>
                            <div className={styles.items}></div>
                            <div className={styles.items}></div>
                            <div className={styles.items}></div>
                        </div>
                </div>

                <div className={styles.allyTeam}>
                    <div>
                        <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img><span>Hai</span>
                    </div>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                </div>
                <div className={styles.allyTeam}>
                    <div>
                        <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}></img><span>Daniel</span>
                    </div>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                    <img src={summonerIcon} alt="Summoner Icon" className={styles.miniIcon}/>
                </div>
                <div className={styles.enemyTeam}>

                </div>
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
        let icon = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/$%7Bdata.icon%7D.jpg'
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