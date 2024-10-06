import { useOptionsContext } from "../hooks/useOptionsContext";
import SidebarOption from "./SidebarOption";
import { useState } from "react";

export default function Sidebar () {
    const { option } = useOptionsContext ()

    return (
        <div className="w-1/5 h-full flex flex-col justify-around items-start">
            <SidebarOption label="PLAY" navPath="/play" isActive={option <= 1} />
            <SidebarOption label="TEAMS" navPath="/teams?leagueId=107254585505459304" isActive={option === 2} />
            <SidebarOption label="PLAYERS" navPath="/players" isActive={option === 3} />
            <SidebarOption label="ABOUT" navPath="/about" isActive={option === 4} />
        </div>
    )
}