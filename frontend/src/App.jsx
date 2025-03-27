import './App.css';
import SearchBar from './components/SearchBar/SearchBar.jsx';
import { useState } from 'react';


function App() {
  const [summonerData, setSummonerData] = useState(null);
  return (
    <div className = "search-main">
        <h1>
          Teemo.gg
        </h1>
        <SearchBar setSummonerData={setSummonerData}/>
    </div>
  );
}

export default App;