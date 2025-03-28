import './App.css';
import SearchBar from './components/SearchBar/SearchBar.jsx';
import { useState } from 'react';
import SummonerCard from './components/SummonerCard/SummonerCard.jsx';

function App() {
  const [summonerData, setSummonerData] = useState(null);
  return (
    <div className = "search-main">
        <h1>
          Teemo.gg
        </h1>
        <SearchBar setSummonerData={setSummonerData}/>
        <SummonerCard data={summonerData}/>
    </div>
  );
}

export default App;