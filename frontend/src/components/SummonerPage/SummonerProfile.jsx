import React from "react";

export default function SummonerInfo({ data }) {
  let lvl = data.level;
  let summonerName = data.summonerName;
  let icon = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${data.icon}.jpg`;
  let tag = data.tag_line;
  return (
    <>
      <div className="w-30 m-4">
        <div className="relative">
          <p className="absolute bottom-25 left-11.5 bg-black text-white rounded-lg border-3 border-black">
            {lvl}
          </p>
          <img
            src={icon}
            alt="Summoner Icon"
            className="aspect-square w-full object-cover border-3 border-black rounded-lg"
          />
        </div>
        <p className="text-center">
            <span className="font-bold text-black">{`${summonerName}`}</span>
            <span className="text-gray-300 font-medium">{`#${tag}`}</span>
        </p>
      </div>
    </>
  );
}
