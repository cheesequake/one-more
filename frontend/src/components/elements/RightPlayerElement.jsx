import { AnimatePresence, motion } from "framer-motion";

import Jett from "../../assets/Jett_icon.webp";
import Raze from "../../assets/Raze_icon.webp";
import Reyna from "../../assets/Reyna_icon.webp";
import Yoru from "../../assets/Yoru_icon.webp";
import Phoenix from "../../assets/Phoenix_icon.webp";
import Neon from "../../assets/Neon_icon.webp";
import Breach from "../../assets/Breach_icon.webp";
import Skye from "../../assets/Skye_icon.webp";
import Sova from "../../assets/Sova_icon.webp";
import Kayo from "../../assets/KAYO_icon.webp";
import Killjoy from "../../assets/Killjoy_icon.webp";
import Cypher from "../../assets/Cypher_icon.webp";
import Sage from "../../assets/Sage_icon.webp";
import Chamber from "../../assets/Chamber_icon.webp";
import Omen from "../../assets/Omen_icon.webp";
import Brimstone from "../../assets/Brimstone_icon.webp";
import Astra from "../../assets/Astra_icon.webp";
import Viper from "../../assets/Viper_icon.webp";
import Fade from "../../assets/Fade_icon.webp";
import Harbor from "../../assets/Harbor_icon.webp";
import Gekko from "../../assets/Gekko_icon.webp";
import Deadlock from "../../assets/Deadlock_icon.webp";
import Iso from "../../assets/Iso_icon.webp";
import Clove from "../../assets/Clove_icon.webp";
import Vyse from "../../assets/Vyse_icon.webp";
import Undefined from "../../assets/Undefined.webp"
import crown from "../../assets/crown.png"

const agentImageMap = {
    "Jett": Jett,
    "Raze": Raze,
    "Reyna": Reyna,
    "Yoru": Yoru,
    "Phoenix": Phoenix,
    "Neon": Neon,
    "Breach": Breach,
    "Skye": Skye,
    "Sova": Sova,
    "Kayo": Kayo,
    "Killjoy": Killjoy,
    "Cypher": Cypher,
    "Sage": Sage,
    "Chamber": Chamber,
    "Omen": Omen,
    "Brimstone": Brimstone,
    "Astra": Astra,
    "Viper": Viper,
    "Fade": Fade,
    "Harbor": Harbor,
    "Gekko": Gekko,
    "Deadlock": Deadlock,
    "Iso": Iso,
    "Clove": Clove,
    "Vyse": Vyse,
    "Undefined": Undefined
};

export default function RightPlayerElement ({ player , isExpanded}) {
    const agentName = player.agent_name ? player.agent_name : "Undefined"
    const agentImage = agentImageMap[agentName]

    return (
        <AnimatePresence>
            <motion.div key={player.assigned_role} className="w-full my-1 flex flex-col justify-start items-start bg-slate-700 bg-opacity-75 py-1">
                <div className="w-full flex justify-start items-center cursor-default" >
                    <div className="bg-slate-600 bg-opacity-75 w-12 flex justify-center items-center">
                        <img src={agentImage} className="w-11" />
                    </div>
                    {isExpanded && <div className="flex flex-col ml-2 justify-between items-center">
                        <div className="flex justify-center items-center font-semibold">
                            {player.in_game_name ? player.in_game_name : ""}
                            { player.in_game_leader === 1 && player.in_game_name && <img src={crown} className="w-4 ml-2" />}
                        </div>
                        <div className="flex justify-center items-center text-teal-200 font-semibold text-xs">
                            {player.in_game_name && "In Party (Competitive)"}
                        </div>
                    </div>}
                </div>
            </motion.div>
        </AnimatePresence>
    )
}