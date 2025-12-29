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
            const nameAndTag = nameSeperate(summonerName);
            try{
                const response = await axios.get(`http://localhost:5000/search_and_send_summoner`, {params: {'summoner_name': nameAndTag.name, 'riot_tag': nameAndTag.tag}});
                setData(response.data);
            } catch(error){
                if(error.response && error.response.status === 404){
                    console.log('Summoner not found in database')
                    try{
                        const post_response = await axios.post('http://localhost:5000/search_and_add_summoner', {'riot_name': nameAndTag.name, 'riot_tag': nameAndTag.tag, 'region': region});
                        console.log(`Successfuly added ${nameAndTag.name}`)
                        setData(post_response.data)
                    } catch(error){
                        console.log(error)
                    }
                } else if(error.request){
                    console.log('Request was sent but no response received')
                }else{
                    console.log("Error fetching users data:", error);
                }
            }
        }
        getSummoner();
    }, [region, summonerName])

    if(Object.keys(data).length === 0){
         return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900">
            <div className="text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500 mx-auto"></div>
                <p className="text-white mt-4">Loading summoner data...</p>
            </div>
        </div>
    );
    }
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