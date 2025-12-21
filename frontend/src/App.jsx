import './App.css';
import Home from './components/Pages/Home.jsx';
import { useState } from 'react';
import SummonerCard from './components/SummonerCard/SummonerCard.jsx';
import { BrowserRouter, Routes, Route} from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/summoners/:region/:summonerName" element={<SummonerCard/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;