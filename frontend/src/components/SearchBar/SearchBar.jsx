import './SearchBar.css';
import React, {useState} from 'react'
export default function SearchBar() {
    const [searchText, setSearchText] = useState("");
    //[isLoading, setIsLoading] = useState(false);

    //const onSearch = async () => {
        // Make request with search text
        /*
        response = axios.get(api_url, searchText);
        do something with response. 
        */
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
            <div></div>
            <input type="text" name = "search" placeholder="Game Name + " size = "50" className="search-bar"></input>
        </div>
      
    );
  }