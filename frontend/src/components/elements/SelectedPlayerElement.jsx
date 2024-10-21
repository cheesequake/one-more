import Jett from "../../assets/Jett_Artwork_Full.webp"
import Raze from "../../assets/Raze_Artwork_Full.webp"
import Reyna from "../../assets/Reyna_Artwork_Full.webp"
import Yoru from "../../assets/Yoru_Artwork_Full.webp"
import Phoenix from "../../assets/Phoenix_Artwork_Full.webp"
import Neon from "../../assets/Neon_Artwork_Full.webp"
import Breach from "../../assets/Breach_Artwork_Full.webp"
import Skye from "../../assets/Skye_Artwork_Full.webp"
import Sova from "../../assets/Sova_Artwork_Full.webp"
import Kayo from "../../assets/KAYO_Artwork_Full.webp"
import Killjoy from "../../assets/Killjoy_Artwork_Full.webp"
import Cypher from "../../assets/Cypher_Artwork_Full.webp"
import Sage from "../../assets/Sage_Artwork_Full.webp"
import Chamber from "../../assets/Chamber_Artwork_Full.webp"
import Omen from "../../assets/Omen_Artwork_Full.webp"
import Brimstone from "../../assets/Brimstone_Artwork_Full.webp"
import Astra from "../../assets/Astra_Artwork_Full.webp"
import Viper from "../../assets/Viper_Artwork_Full.webp"
import Fade from "../../assets/Fade_Artwork_Full.webp"
import Harbor from "../../assets/Harbor_Artwork_Full.webp"
import Gekko from "../../assets/Gekko_Artwork_Full.webp"
import Deadlock from "../../assets/Deadlock_Artwork_Full.webp"
import Iso from "../../assets/Iso_Artwork_Full.webp"
import Clove from "../../assets/Clove_Artwork_Full.webp"
import Vyse from "../../assets/Vyse_Artwork_Full.webp"
import crown from "../../assets/crown.png"
import active from "../../assets/active.png"
import StatKeyValueElement from "./StatKeyValueElement"

const agentImageMap = {
    "Jett": Jett,
    "Raze": Raze,
    "Reyna": Reyna,
    "Yoru": Yoru,
    "Phoenix": Phoenix
}

export default function SelectedPlayerElement ({ player }) {

    if (!player || !player.in_game_name) {
        return (
            <div className="w-full h-full border-l border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25 cursor-default text-8xl font-Tungsten flex justify-center items-center">
                <div className="text-center w-2/3">
                    <span className="text-primary-riot inline">SELECT</span> A PLAYER TO VIEW THEIR <span className="text-primary-riot inline">STATS</span>
                </div>
            </div>
        )
    }
    const agentImage = agentImageMap[player.agent_name]

    return (
        <div className="w-full h-full border-l flex justify-between items-center border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25 cursor-default">
            <div className="flex h-full flex-col justify-start items-start p-4 text-white">
                <div className="border-b-2 border-b-primary-riot py-3">
                    <div className="font-bold text-4xl">
                        {player.team_acronym +" "+ player.in_game_name}
                    </div>
                    <div className="font-light text-lg flex items-center">
                        {player.real_name} {player.in_game_leader && <img src={crown} className="h-4 ml-2" />} {player.status === "Active" && <img src={active} className="h-4 ml-2" />}
                    </div>
                </div>
                <StatKeyValueElement stat="Games Played: " value={player.total_matches_played} />
                <StatKeyValueElement stat="Total Kills/Deaths/Assists: " value={player.total_kills+"/"+player.total_deaths+"/"+player.total_assists} />
                <StatKeyValueElement stat="Attacking KDA: " value={player.attack_KDA} />
                <StatKeyValueElement stat="Defending KDA: " value={player.defense_KDA} />
                <StatKeyValueElement stat="ACS: " value={player.average_combat_score} />
                <StatKeyValueElement stat="Headshot %: " value={player.headshot_percentage} />
                <StatKeyValueElement stat="Average Attack FK/FD: " value={player.average_attack_first_kills+"/"+player.average_attack_first_deaths} />
                <StatKeyValueElement stat="Average Defense FK/FD: " value={player.average_defense_first_kills+"/"+player.average_defense_first_deaths} />
                <StatKeyValueElement stat="Average Attack FK/FD: " value={player.average_attack_first_kills+"/"+player.average_attack_first_deaths} />
                <StatKeyValueElement stat="Aces: " value={player.aces} />
                <StatKeyValueElement stat="4Ks: " value={player.four_kills} />
                <StatKeyValueElement stat="Operator Kills: " value={player.operator_kills} />
                <StatKeyValueElement stat="Pistol Kills: " value={player.pistol_kills} />
            </div>
            <div className="h-full flex flex-col justify-start items-center">
                <img src={agentImage} className="h-13/16" />
                <div className="flex flex-col justify-start items-center text-white">
                    <StatKeyValueElement stat="Most Played Agent: " value={player.agent_name} />
                    <StatKeyValueElement stat={`KDA as ${player.agent_name}: `} value={player.KDA_ratio} />
                </div>
            </div>
        </div>
    )
}