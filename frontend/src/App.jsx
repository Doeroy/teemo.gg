import './App.css';
import Home from './components/Pages/Home.jsx';
import { useState } from 'react';
import SummonerPage from './components/Pages/SummonerPage.jsx';
import { BrowserRouter, Routes, Route} from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/summoners/:region/:summonerName" element={<SummonerPage/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;