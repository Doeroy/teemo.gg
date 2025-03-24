import './SearchBar.css';
import React, {useState} from 'react'
import {FaSearch} from "react-icons/fa"
import axios from 'axios';

export default function SearchBar() {
    const [searchText, setSearchText] = useState("");
    const [region, setRegion] = useState("NA1")
    //[isLoading, setIsLoading] = useState(false);

    //const onSearch = async () => {
        // Make request with search text
        /*
        response = axios.get(api_url, searchText);
        do something with response. 
        */
    
    function handleChange(value){
        setSearchText(value);
    }

    function  isAlphanumeric(str){ 
      return /^[a-z0-9]+$/i.test(str);
    }
    const riotInfo = {
          summonerID: searchText,
          riotID: "",
          riot_tag: "",
          region: "",
        };

    const fetchData = async (value) => {
      try{
        const response = await fetch("http://localhost:5000/summoners"); //makes a call to summoners endpoint
        if (response.ok){ //if the respose status is in the range 200-299 response.ok returns true. Else False  
          const data = await response.json(); //converts response to json
          let userFound = false;
          const splitId = searchText.split('#').map(i => i.trim());
          riotInfo.summonerID = splitId[0];
          riotInfo.riot_tag = splitId[1];
          riotInfo.region = region;
          if(!isAlphanumeric(riotInfo.summonerID) || riotInfo.summonerID.length < 3  || riotInfo.summonerID.length > 16){
            throw new Error("Summoner ID (Game Name) must be between 3-16 alphanumeric characters");
          }
          if(!isAlphanumeric(riotInfo.riot_tag) || riotInfo.riot_tag.length < 3 || riotInfo.riot_tag.length > 5){
            throw new Error("Tagline must be between 3-5 alphanumeric characters");
          }
          riotInfo.riotID = `${riotInfo.summonerID}#${riotInfo.riot_tag}`
          console.log(riotInfo)
          //console.log(`summoner: ${riotInfo.summonerID} region: ${riotInfo.riot_tag}`);
          for(let i = 0; i < data.length; i++){
            //console.log(`region: ${data[i].riot_tag}`);
            if((value.target.value === data[i].summonerID) && data[i].riot_tag === region){
              console.log(`Found Summoner: ${value.target.value} Region: ${data[i].region}`);
              userFound = true; 
              //change this to have it recieve a call from the backend
            }
          }
          if(userFound === false){
            //make sure to verify that the user is in the Riot API
            //createPost()
          }
        } 
        else {
          throw new Error('Response was not between 200-299'); //if the response was not a 200 then we throw an error
        }
      } catch(error){ //error object that gets thrown if anything in the try block fails
        console.error("Failed to fetch summoners:", error) //prints out the error in console
      }
    }

    const createPost = async () => {
      try{
        await axios.post("http://localhost:5000/add_summoner", riotInfo);
      }catch(e){
        if(e.response){
          console.error(`Response error: ${e.response}`)
        } else {
          // Something went wrong setting up the request
          console.error(`Error: ${e.response}`);
        } 
      };
    };
    
    function isEnter(event){
        if(event.key === "Enter"){
          fetchData(event)
        }
    }

    return (
        <div className = "search-container">
          <div className = "input-wrapper">
            <form value = {region} onChange = {(e) => setRegion(e.target.value)}>
              {/* when you handle an event, React gives you back an event object. The event contains
                the element that was changed and the current value of that element
              */}
              <select name = "region-dropdown">
                <option value="NA1">NA</option>
                <option value="EUW1">EUW</option>
                <option value="EUNE1">EUN</option>
                <option value="KR">KR</option>
                <option value="JP1">JP</option>
                <option value="OC1">OCE</option>
                <option value="VN2">VN</option>
              </select>
            </form> 
            <input type="text" 
            value = {searchText} 
            name = "search" 
            onKeyDown = {isEnter} 
            onChange = {e => handleChange(e.target.value)} 
            placeholder= "Game Name + " 
            size = "50" 
            className="search-bar">
            </input>
            <FaSearch id="search-icon"/>  
            </div>
        </div>
      
    );
  }