import './SearchBar.css';
import React, {useState} from 'react'
import {FaSearch} from "react-icons/fa"
import axios from 'axios';

export default function SearchBar({ setSummonerData }) {
    const [searchText, setSearchText] = useState("");
    const [region, setRegion] = useState("NA1")
    const [status, setStatus] = useState('Idle')
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

  function isAlphanumericName(str) {
    return /^[a-z0-9 ]+$/i.test(str);
  }

  function isAlphanumericTag(str){
    return /^[a-z0-9]+$/i.test(str);
  }
  const createPost = async () => {
    try{
      const response = await axios.post("http://localhost:5000/search_and_add_summoner", riotInfo);
      console.log(`Success: ${response.status}`)
      return {success: true, error: null}
    }catch(e){
      if(e.response && e.response.status == 404){
        setStatus('Summoner not found');
        return { success: false, error: 'not_found' };
      }
      else if(e.response){
        console.error(`Response error: ${e.response}`)
        return { success: false, error: 'response_error' };
      } else {
        console.error(`Error: ${e}`);
        return { success: false, error: 'unknown' };
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
      
  const fetchData = async () => {
    try{
      const response = await axios.get("http://localhost:5000/search_and_send_summoner", {params: riotInfo}); //makes a call to summoners endpoint
      console.log(response.data)
      console.log(response.status)
      setStatus('Found')
      }catch(error){ //error object that gets thrown if anything in the try block fails
        if(error.response && error.response.status == 404){ //sometimes we don't get an error.response so we need to check for it so the if statement doesn't break
          try{
            console.log("Summoner wasn't found in the database. Attempting to add summoner")
            const add_result = await createPost()
            if(add_result.success){
              console.log('Successfully added summoner!')
              setStatus('Added')
            } else if(add_result.error == 'not_found'){
              console.error('Error Status: 404. Summoner does not exist')
            }else {
              setStatus('Error');
            }
          }
          catch(addError) {
            console.error("Failed to add summoner: ", addError);
            setStatus('Error');
          }
          }else{
          console.error("Failed to fetch summoner:", error) //prints out the error in console
          setStatus('Error')
          }
      }
  }

  function isEnter(event){
      if(event.key === "Enter"){
        const splitId = searchText.split('#').map(i => i.trim());
        riotInfo.summonerID = splitId[0];
        riotInfo.riot_tag = splitId[1];
        riotInfo.region = region;
        riotInfo.riot_id = ''
        riotInfo.puuid = "balls" // temporary dummy value
        if(!isAlphanumericName(riotInfo.summonerID) || riotInfo.summonerID.length < 3  || riotInfo.summonerID.length > 16){
          alert("Summoner ID (Game Name) must be between 3-16 alphanumeric characters");
          return;
        }
        if(!isAlphanumericTag(riotInfo.riot_tag) || riotInfo.riot_tag.length < 3 || riotInfo.riot_tag.length > 5){
          alert("Tagline must be between 3-5 alphanumeric characters");
          return;
        }
        else{
          setStatus('Loading')
          fetchData()
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
            <p>{status}</p>
        </div>
      
    );
  }