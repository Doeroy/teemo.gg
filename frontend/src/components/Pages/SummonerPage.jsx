import React, { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import { nameSeperate } from "../../utils/nameValidation";
import SummonerCard from "../SummonerPage/SummonerCard";
import SummonerInfo from "../SummonerPage/SummonerProfile";

import axios from "axios";
function SummonerPage(){
    const { region, summonerName } = useParams();
    const [data, setData] = useState({})
    console.log(summonerName)
    useEffect(() => {
        const getSummoner = async () => {
            try{
                const nameAndTag = nameSeperate(summonerName);
                const response = await axios.get(`http://localhost:5000/search_and_send_summoner`, {params: {'summoner_name': nameAndTag.name, 'riot_tag': nameAndTag.tag}});
                setData(response.data);
            } catch(error){
                console.log("Error fetching users data:", error);
            }
        }
        getSummoner();
    }, [region, summonerName])
    return(
        <div className="bg-[url('../../../public/images/ashe.png')] min-h-screen bg-cover bg-center bg-no-repeat bg-fixed p-4">
            <div>
                <SummonerInfo data={data}/>
            </div>
            <div className="flex justify-center">
                <SummonerCard data={data}/>
            </div>
        </div>
    )
}

export default SummonerPage;