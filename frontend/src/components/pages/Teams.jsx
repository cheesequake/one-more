import axios from "axios"
import { useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import TeamElement from "../elements/TeamElement"
import loadingAnimation from "../../assets/LoadingAnimation.gif"

export default function Teams () {
    const [league, setLeague]= useState (null)
    const [teams, setTeams] = useState ([])
    const [leagues, setLeagues] = useState ([])
    const [filteredTeams, setFilteredTeams] = useState (teams)
    const [searchTerm, setSearchTerm] = useState ("")
    const [isLoading, setIsLoading] = useState (true)
    const [showOverlay, setShowOverlay] = useState (false)
    const location = useLocation ()
    const navigate = useNavigate ()

    useEffect (() => {
        const getLeagues = async () => {
            try {
                const leaguesResponse = await axios.get (import.meta.env.VITE_BACKEND_URL+`leagues`)
                setLeagues (leaguesResponse.data.leagues)
            }
            catch {
                console.log ("Error getting leagues")
            }
        }

        getLeagues ()
    }, [])

    useEffect (() => {
        const searchParams = new URLSearchParams (location.search)
        const leagueId = searchParams.get ('leagueId')
        setIsLoading (true)
        const getLeagueData = async (leagueId) => {
            try {
                const leagueResponse = await axios.get (import.meta.env.VITE_BACKEND_URL+`leagues/${leagueId}`)
                setLeague (leagueResponse.data)
                const teamResponse = await axios.get (import.meta.env.VITE_BACKEND_URL+`teams?leagueId=${leagueId}`)
                setTeams (teamResponse.data)
                setIsLoading (false)
            }
            catch (error) {
                console.log (error)
            }
        }

        if (!leagueId) {
            // If leagueID is missing, navigate to the same path with the parameter set to 12
            searchParams.set('leagueId', '107254585505459304')
            navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true, state: {} });
        }
        else {
            getLeagueData (leagueId)
        }
    }, [location.search])

    useEffect (() => {
        const filtered = teams.filter (team =>
            team.team_name.toLowerCase().includes(searchTerm.toLowerCase())
        )
        setFilteredTeams (filtered)
    }, [searchTerm, teams])

    const handleLeagueChange = () => {
        setShowOverlay (true)
    }

    return (
        <>
            {showOverlay &&
            <motion.div
            key="leaguesOverlay"
            className="w-screen h-screen min-h-screen flex justify-center items-center absolute top-0 left-0 z-10 backdrop-blur-lg"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, stiffness: 0 }}
            onClick={() => {setShowOverlay (false)}}>
                <div className="h-5/6 w-5/6 flex flex-wrap justify-center items-center overflow-y-scroll bg-secondary-riot rounded-lg" onClick={(e) => {e.stopPropagation()}}>
                    {leagues.map ((league) => (
                        <div className="flex flex-wrap p-2 m-1 cursor-pointer justify-center hover:bg-slate-950 hover:border-slate-600 duration-100 items-center border border-white rounded-md" key={league.league_id} onClick={() => {
                                setLeague (league)
                                setShowOverlay (false)
                                navigate (`/teams?leagueId=${league.league_id}`)
                            }}>
                            <img src={league.league_logo_url} className="h-4" />
                            <div className="ml-1 text-white">{league.league_name}</div>
                        </div>
                ))}
                </div>
            </motion.div>}
            <div className="w-11/12 h-15/16 flex flex-col justify-start items-center">
                <div className="flex w-full justify-between items-center">
                    <div className="w-10/12">
                        <input type="text" className="w-full h-10 rounded-sm px-2 bg-white bg-opacity-75 focus:border-2 focus:border-primary-riot focus:outline-none" placeholder="Filter results" value={searchTerm} onChange={(e) => {setSearchTerm (e.target.value)}} />
                    </div>
                    <div className="flex justify-center items-center text-white bg-secondary-riot bg-opacity-75 hover:bg-opacity-100 duration-100 rounded-sm h-10 px-2 cursor-pointer border hover:border-primary-riot" onClick={handleLeagueChange}>
                        {!isLoading ? <>
                            <img src={league.league_logo_url} className="h-8" />
                            <div className="ml-2">{league.league_name}</div>
                        </> : <><img className="h-full" src={loadingAnimation} /></> }
                    </div>
                </div>
                <div className="w-full flex flex-wrap items-start overflow-y-scroll">
                    {!isLoading ? filteredTeams.map ((team) => (
                        <TeamElement key={team.team_id} team={team} />
                    )) : <div className="w-full h-full flex justify-center items-center"><img className="h-1/3" src={loadingAnimation} /></div>}
                </div>
            </div>
        </>
    )
}