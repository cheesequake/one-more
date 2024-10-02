import { useNavigate } from "react-router-dom"
import { useOptionsContext } from "../hooks/useOptionsContext"
import dot from "../assets/dot.png"

export default function SidebarOption ({ label, navPath, isActive }) {
    const navigate = useNavigate ()
    const { dispatch } = useOptionsContext ()

    const handleClick = () => {
        switch (label) {
            case "PLAY":
                dispatch ({ type: 'SET', payload: 1 })
                navigate (navPath)
                break;
            case "TEAMS":
                dispatch ({ type: 'SET', payload: 2 })
                navigate (navPath)
                break;
            case "PLAYERS":
                dispatch ({ type: 'SET', payload: 3 })
                navigate (navPath)
                break;
            case "ABOUT":
                dispatch ({ type: 'SET', payload: 4 })
                navigate (navPath)
                break;
            default:
                break;
        }
    }

    return (
        <>
            <div className="flex font-Tungsten text-7xl items-center">
                <img src={dot} className="w-4 h-4 ml-2 mr-8" />
                <span className={isActive ? "text-primary-riot cursor-pointer" : "text-white cursor-pointer"} onClick={handleClick}>{label}</span>
            </div>
        </>
    )
}