import './SearchBar.css';
import React, {useState} from 'react'
import {FaSearch} from "react-icons/fa"
export default function SearchBar() {
    const [searchText, setSearchText] = useState("");
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

    const fetchData = async (value) => {
      try{
        const response = await fetch("http://localhost:5000/summoners"); //makes a call to summoners endpoint
        if (response.ok){
          const data = await response.json(); //converts response to json
          console.log(data); 
        } 
        else {
          throw new Error('Failed to fetch summoner:'); //if the response was not a 200 then we throw an error
        }
      } catch(error){ //error object that gets thrown if anything in the try block fails
        console.error("Failed to fetch summoners:", error) //prints out the error in console
      }
    }

    function isEnter(event){
        if(event.key == "Enter"){
          alert(searchText);
          fetchData(event)
        }
    }

    return (
        <div className = "search-container">
          
            <form class = "region-dropdown" >
              <select name = "region-tag">
                <option value="NA1">NA</option>
                <option value="EUW1">EUW</option>
                <option value="EUNE1">EUN</option>
                <option value="KR">KR</option>
                <option value="JP1">JP</option>
                <option value="OC1">OCE</option>
                <option value="OC1">VN</option>
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
      
    );
  }