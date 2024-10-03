import light_logo from "../assets/one-more-light.png"
import muted_icon from "../assets/muted.png"
import unmuted_icon from "../assets/unmuted.png"
import { useNavigate } from "react-router-dom"
import { useOptionsContext } from "../hooks/useOptionsContext"

export default function Navbar ({ muted, setMuted }) {
    const navigate = useNavigate ()
    const {dispatch} = useOptionsContext ()

    const handleMute = () => {
        if (muted) {
            setMuted (false)
        }
        else {
            setMuted (true)
        }
    }

    const handleClick = () => {
        dispatch ({ type: 'SET', payload: 0 })
        navigate ("/")
    }

    return (
        <div className="w-full min-h-10vh h-10vh flex justify-between items-center px-2 py-1">
            <img src={light_logo} className="h-10 cursor-pointer" onClick={handleClick} />
            <button onClick={handleMute} className="h-10 rounded-lg border-2 border-white p-2">
                <img src={muted ? muted_icon : unmuted_icon} className="h-6 w-6" />
            </button>
        </div>
    )
}