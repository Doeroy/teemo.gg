import React, {useState} from 'react'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../SearchBar/SearchBar';
const Home = () =>  {
  return(
    <div className="bg-[url('../../../public/images/zeri-winter-wonder-splash-art.jpg')] bg-cover bg-center h-screen flex flex-col justify-center">
      <main className='flex-1 flex items-center justify-center'>
        <SearchBar/>
      </main>
      <footer class="w-full py-6 px-4 bg-slate-900/60 backdrop-blur-md border-t border-white/10 text-slate-400 text-xs text-center">
        <div class="max-w-6xl mx-auto">
          <p>
            Teemo.gg isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default Home