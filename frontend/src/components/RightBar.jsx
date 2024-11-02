import { useEffect, useRef, useState } from "react"
import { useTeamContext } from "../hooks/useTeamContext"
import { AnimatePresence, motion } from "framer-motion";
import RightPlayerElement from "./elements/RightPlayerElement";

export default function RightBar () {
    const { team } = useTeamContext ()
    const [isExpanded, setIsExpanded] = useState (false)
    const ref = useRef(null);
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (ref.current && !ref.current.contains(event.target)) {
                setIsExpanded(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    const toggleExpand = () => {
        setIsExpanded((prev) => !prev);
    };

    return (
        <AnimatePresence>
            <motion.div
                key="teamOverlay"
                ref={ref}
                onClick={toggleExpand}
                initial={{ width: "48px" }}
                animate={{ width: isExpanded ? "200px" : "48px" }}
                transition={{ duration: 0.3 }}
                className="h-90vh min-h-90vh max-h-90vh flex flex-col justify-start items-start bg-slate-800 bg-opacity-85 hover:bg-opacity-100 duration-200 z-50 absolute right-0 text-white font-light"
            >
                {team && 
                <div className="font-FF-Mark w-full flex justify-around items-start bg-slate-900 py-2">
                    <div>
                        {team.length}
                    </div>
                    {isExpanded && <>
                    <div>
                        TEAM
                    </div>
                    <div>

                    </div></>}
                </div>}
                {team && team.map ((player, index) => {
                    return (
                        <RightPlayerElement key={index} player={player} isExpanded={isExpanded} />)
                })}
            </motion.div>
        </AnimatePresence>
    )
}