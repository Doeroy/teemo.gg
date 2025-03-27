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

const createPost = async () => {
  try{
    const response = await axios.post("http://localhost:5000/search_and_add_summoner", riotInfo);
    console.log(`Success: ${response.status}`)
  }catch(e){
    if(e.response){
      console.error(`Response error: ${e.response}`)
    } else {
      // Something went wrong setting up the request
      console.error(`Error: ${e.response}`);
    } 
  };
};

const riotInfo = {
  summonerID: searchText,
  riot_id: "",
  riot_tag: "",
  region: "",
  puuid: ""
};
    
const fetchData = async (value) => {
  try{
    //let userFound = false;
    /*
      need to add an if statement to see if the user is already 
    */
    const response = await axios.get("http://localhost:5000/summoners"); //makes a call to summoners endpoint
     //if the respose status is in the range 200-299 response.ok returns true. Else False  
      console.log(riotInfo)
      console.log(response.data)
      //userFound = true;
    
    /*
    else if(!userFound){
      console.log('ballsack')
    }
    */
    if(response.status > 299) {
      throw new Error('Response was not between 200-299'); //if the response was not a 200 then we throw an error
    }
  } catch(error){ //error object that gets thrown if anything in the try block fails
    console.error("Failed to fetch summoners:", error) //prints out the error in console
  }
}

function isEnter(event){
    if(event.key === "Enter"){
      const splitId = searchText.split('#').map(i => i.trim());
      riotInfo.summonerID = splitId[0];
      riotInfo.riot_tag = splitId[1];
      riotInfo.region = region;
      riotInfo.riot_id = `${riotInfo.summonerID}#${riotInfo.riot_tag}`
      riotInfo.puuid = "temp" // temporary dummy value
      if(!isAlphanumeric(riotInfo.summonerID) || riotInfo.summonerID.length < 3  || riotInfo.summonerID.length > 16){
        alert("Summoner ID (Game Name) must be between 3-16 alphanumeric characters");
        return;
      }
      if(!isAlphanumeric(riotInfo.riot_tag) || riotInfo.riot_tag.length < 3 || riotInfo.riot_tag.length > 5){
        alert("Tagline must be between 3-5 alphanumeric characters");
        return;
      }
      else{
        fetchData(event)
      }
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
            placeholder= "Game Name + Tag" 
            size = "50" 
            className="search-bar">
            </input>
            <FaSearch id="search-icon"/>  
            </div>
        </div>
      
    );
  }