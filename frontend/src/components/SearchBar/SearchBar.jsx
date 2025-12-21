import React, { useState } from "react";
import { FaSearch } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { CircleFlag } from 'react-circle-flags'

const SearchBar = () => {
  const [search, setSearch] = useState();
  return (
    <div className="flex items-center w-full max-w-2xl bg-white/10 backdrop-blur-xl border border-white/20 rounded-full px-6 py-4 shadow-2xl focus-within:ring-2 focus-within:ring-blue-500/50 transition-all">
      <div className="flex items-center gap-2 border-r border-white/20 pr-4 mr-4 text-white font-medium cursor-pointer">
        <div className="w-5 h-5 rounded-sm">
          <CircleFlag countryCode="us"/>
        </div>
        <span>NA</span>
      </div>

      <input
        type="text"
        placeholder="Search Summoner Name..."
        class="bg-transparent w-full text-white placeholder-white/50 outline-none text-lg"
      />
    </div>
  );
};

export default SearchBar;
