import React, { useState } from "react";
import { FaSearch } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { CircleFlag } from "react-circle-flags";
import { nameSeperate } from "../../utils/nameValidation";
const regions = [
  {
    region: "NA",
    code: "us",
    platform: "na1"
  },
  {
    region: "KR",
    code: "kr",
    platform: "kr"
  },
  {
    region: "JP",
    code: "jp",
    platform: "jp1"
  },
  {
    region: "VN",
    code: "vn",
    platform: "vn2"
  },
];

const SearchBar = () => {
  const [search, setSearch] = useState("");
  const [region, setRegion] = useState("NA");
  const [regionCode, setRegionCode] = useState("us");
  const [dropDown, setDropDown] = useState(false);
  const [regionPlatform, setRegionPlatform] = useState("na1")
  const [error, setError] = useState("");
  const navigate = useNavigate();

  return (
    <div className="w-full flex flex-col items-center relative">
      <div className="relative flex items-center w-full max-w-2xl bg-white/10 backdrop-blur-xl border border-white/20 rounded-full px-6 py-4 shadow-2xl focus-within:ring-2 focus-within:ring-blue-500/50 transition-all">
        <div className="flex items-center gap-2 border-r border-white/20 pr-4 mr-4 text-white font-medium cursor-pointer">
          <div className="w-5 h-5 rounded-sm">
            <CircleFlag countryCode={regionCode} />
          </div>
          <button
            className="bg-transparent text-white font-medium outline-none cursor-pointer pr-6"
            onClick={() => {
              setDropDown(!dropDown);
            }}
            aria-label={`Select region, currently ${region}`}
            aria-expanded={dropDown}
            aria-haspopup="true"
          >
            {region}
          </button>
        </div>

        <input
          aria-label="Search summoner by name and tag"
          type="text"
          placeholder="Search Summoner Name..."
          className="bg-transparent w-full text-white placeholder-white/50 outline-none text-lg"
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              const nameTag = nameSeperate(search);
              if (nameTag.error === false) {
                const encodedName = encodeURIComponent(`${nameTag.name.trim()}#${nameTag.tag}`);
                navigate(`/summoners/${regionPlatform}/${encodedName}`);
              } else {
                setError(
                  "Please enter a valid summoner name (EX: Player#NA1)"
                );
              }
            }
          }}
        />
        <div className="absolute top-full mt-2 left-0 w-48 rounded-lg shadow-xl overflow-hidden">
          {dropDown &&
            regions.map((region) => (
              <button
                type="button"
                className="w-full text-left bg-blue-950 p-4 cursor-pointer flex gap-2 text-white hover:bg-blue-500"
                key={region.code}
                onClick={() => {
                  setRegion(region.region);
                  setRegionCode(region.code);
                  setRegionPlatform(region.regionPlatform)
                  setDropDown(false);
                }}
              >
                <div className="w-5 h-5 rounded-sm">
                  <CircleFlag countryCode={region.code} />
                </div>
                {region.region}
              </button>
            ))}
        </div>
      </div>
      <p className="absolute top-full mt-2 text-red-500 text-md font-extrabold text-shadow-sm">
        {error}
      </p>
    </div>
  );
};

export default SearchBar;
