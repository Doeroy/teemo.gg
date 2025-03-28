import './SummonerCard.css';
import React, {useState} from 'react'

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
            <img src={icon} alt="Summoner Icon" id ="summonerIcon"></img>
            <h3>{`${summonerName}#${tag}`}</h3>
        </div>
    );
}