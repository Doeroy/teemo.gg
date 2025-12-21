import './App.css';
import SearchBar from './components/SearchBar/SearchBar.jsx';
import { useState } from 'react';
import SummonerCard from './components/SummonerCard/SummonerCard.jsx';
import { BrowserRouter, Routes, Route} from 'react-router-dom';

function App() {
  const [summonerData, setSummonerData] = useState(null);
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SearchBar setSummonerData={setSummonerData}/>} />
        <Route path="/summoners/:region/:summonerName" element={<SummonerCard data={summonerData}/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;