import PlayerElement from "../elements/PlayerElement"
import loadingAnimation from "../../assets/LoadingAnimation.gif"
import { useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import filterIcon from "../../assets/filter-icon.png"
import SelectedPlayerElement from "../elements/SelectedPlayerElement"

export default function Players () {
    const [searchTerm, setSearchTerm] = useState ("")
    const [players, setPlayers] = useState ([])
    const [selectedPlayer, setSelectedPlayer] = useState({})
    const [filteredPlayers, setFilteredPlayers] = useState (players)
    const [isLoading, setIsLoading] = useState (true)
    const [showOverlay, setShowOverlay] = useState (false)
    const location = useLocation ()
    const navigate = useNavigate ()

    const searchParams = new URLSearchParams(location.search);

    const [filters, setFilters] = useState({
        level: searchParams.get('level') || 'professional',
        igl: searchParams.get('igl') || 'any',
        role: searchParams.get('role') || 'duelist',
        sortBy: searchParams.get('sortBy') || 'name',
        sortOrder: searchParams.get('sortOrder') || 'ASC',
    });

    useEffect (() => {
        const level = searchParams.get ('level')
        const igl = searchParams.get ('igl')
        const role = searchParams.get ('role')
        const sortBy = searchParams.get ('sortBy')
        const sortOrder = searchParams.get ('sortOrder')
        const allowedLevels = ["professional", "semi-professional", "game-changer"]
        const allowedIgls = ["yes", "no", "any"]
        const allowedRoles = ["duelist", "initiator", "controller", "sentinel"]
        const allowedSortBy = ["name", "attacking-kda", "defending-kda", "kills", "deaths", "assists", "year", "team"]
        const allowedSortOrder = ["ASC", "DESC"]
        let updated = false

        setIsLoading (true)
        const getData = async () => {
            try {
                // const playerResponse = await axios.get (import.meta.env.VITE_BACKEND_URL+`players/`)
                // setPlayers (playerResponse.data)
                const playerResponse = {
                    data: [
                        {
                            "player_id": 1,
                            "real_name": "Alice Johnson",
                            "in_game_name": "A1ce",
                            "status": "Inctive",
                            "home_team_id": 101,
                            "attack_KDA": 1.75,
                            "defense_KDA": 1.50,
                            "total_kills": 350,
                            "total_deaths": 200,
                            "total_assists": 100,
                            "aces": 5,
                            "four_kills": 10,
                            "operator_kills": 15,
                            "average_combat_score": 250.50,
                            "pistol_kills": 50,
                            "total_matches_played": 100,
                            "level": "Professional",
                            "in_game_leader": false,
                            "headshot_percentage": 45.00,
                            "average_attack_first_kills": 0.40,
                            "average_attack_first_deaths": 0.30,
                            "average_defense_first_kills": 0.35,
                            "average_defense_first_deaths": 0.25,
                            "gender": "Female",
                            "team_acronym": "T1",
                            "team_logo_url": "http://example.com/logo1.png",
                            "team_name": "Team Alpha",
                            "agent_id": "agent1",
                            "agent_name": "Jett",
                            "agent_role": "duelist",
                            "matches_played": 60,
                            "KDA_ratio": 1.80
                        },
                        {
                            "player_id": 2,
                            "real_name": "Bob Smith",
                            "in_game_name": "Bobster",
                            "status": "Active",
                            "home_team_id": 102,
                            "attack_KDA": 1.60,
                            "defense_KDA": 1.40,
                            "total_kills": 300,
                            "total_deaths": 220,
                            "total_assists": 90,
                            "aces": 3,
                            "four_kills": 5,
                            "operator_kills": 10,
                            "average_combat_score": 240.75,
                            "pistol_kills": 45,
                            "total_matches_played": 95,
                            "level": "Professional",
                            "in_game_leader": true,
                            "headshot_percentage": 47.50,
                            "average_attack_first_kills": 0.38,
                            "average_attack_first_deaths": 0.32,
                            "average_defense_first_kills": 0.30,
                            "average_defense_first_deaths": 0.20,
                            "gender": "Male",
                            "team_acronym": "T2",
                            "team_logo_url": "http://example.com/logo2.png",
                            "team_name": "Team Beta",
                            "agent_id": "agent2",
                            "agent_name": "Reyna",
                            "agent_role": "duelist",
                            "matches_played": 58,
                            "KDA_ratio": 1.75
                        },
                        {
                            "player_id": 3,
                            "real_name": "Charlie Brown",
                            "in_game_name": "C.Brown",
                            "status": "Active",
                            "home_team_id": 103,
                            "attack_KDA": 1.85,
                            "defense_KDA": 1.55,
                            "total_kills": 400,
                            "total_deaths": 210,
                            "total_assists": 120,
                            "aces": 7,
                            "four_kills": 12,
                            "operator_kills": 20,
                            "average_combat_score": 270.80,
                            "pistol_kills": 60,
                            "total_matches_played": 110,
                            "level": "Professional",
                            "in_game_leader": true,
                            "headshot_percentage": 50.00,
                            "average_attack_first_kills": 0.42,
                            "average_attack_first_deaths": 0.25,
                            "average_defense_first_kills": 0.37,
                            "average_defense_first_deaths": 0.28,
                            "gender": "Male",
                            "team_acronym": "T3",
                            "team_logo_url": "http://example.com/logo3.png",
                            "team_name": "Team Gamma",
                            "agent_id": "agent1",
                            "agent_name": "Jett",
                            "agent_role": "duelist",
                            "matches_played": 70,
                            "KDA_ratio": 1.90
                        },
                        {
                            "player_id": 4,
                            "real_name": "Diana Prince",
                            "in_game_name": "WonderD",
                            "status": "Active",
                            "home_team_id": 101,
                            "attack_KDA": 1.70,
                            "defense_KDA": 1.60,
                            "total_kills": 320,
                            "total_deaths": 230,
                            "total_assists": 80,
                            "aces": 4,
                            "four_kills": 8,
                            "operator_kills": 12,
                            "average_combat_score": 255.30,
                            "pistol_kills": 40,
                            "total_matches_played": 85,
                            "level": "Professional",
                            "in_game_leader": true,
                            "headshot_percentage": 48.00,
                            "average_attack_first_kills": 0.39,
                            "average_attack_first_deaths": 0.31,
                            "average_defense_first_kills": 0.33,
                            "average_defense_first_deaths": 0.22,
                            "gender": "Female",
                            "team_acronym": "T1",
                            "team_logo_url": "http://example.com/logo1.png",
                            "team_name": "Team Alpha",
                            "agent_id": "agent3",
                            "agent_name": "Phoenix",
                            "agent_role": "duelist",
                            "matches_played": 55,
                            "KDA_ratio": 1.80
                        },
                        {
                            "player_id": 5,
                            "real_name": "Eve Adams",
                            "in_game_name": "Eve_A",
                            "status": "Active",
                            "home_team_id": 102,
                            "attack_KDA": 1.65,
                            "defense_KDA": 1.45,
                            "total_kills": 290,
                            "total_deaths": 210,
                            "total_assists": 95,
                            "aces": 2,
                            "four_kills": 4,
                            "operator_kills": 8,
                            "average_combat_score": 245.00,
                            "pistol_kills": 30,
                            "total_matches_played": 90,
                            "level": "Professional",
                            "in_game_leader": true,
                            "headshot_percentage": 44.00,
                            "average_attack_first_kills": 0.37,
                            "average_attack_first_deaths": 0.29,
                            "average_defense_first_kills": 0.34,
                            "average_defense_first_deaths": 0.26,
                            "gender": "Female",
                            "team_acronym": "T2",
                            "team_logo_url": "http://example.com/logo2.png",
                            "team_name": "Team Beta",
                            "agent_id": "agent2",
                            "agent_name": "Reyna",
                            "agent_role": "duelist",
                            "matches_played": 50,
                            "KDA_ratio": 1.70
                        }
                    ]
                }
                setPlayers (playerResponse.data)

                setIsLoading (false)
            }
            catch (error) {
                console.log (error)
            }
        }

        if (!level || !allowedLevels.includes(level)) {
            searchParams.set('level', 'professional')
            updated = true
        }

        if (!igl || !allowedIgls.includes(igl)) {
            searchParams.set('igl', 'any')
            updated = true
        }

        if (!role || !allowedRoles.includes(role)) {
            searchParams.set('role', 'duelist')
            updated = true
        }

        if (!sortBy || !allowedSortBy.includes(sortBy)) {
            searchParams.set('sortBy', 'name')
            updated = true
        }

        if (!sortOrder || !allowedSortOrder.includes(sortOrder)) {
            searchParams.set('sortOrder', 'ASC')
            updated = true
        }

        if (updated) {
            navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true, state: {} });
        }
        else {
            getData ()
        }
    }, [location.search])

    useEffect (() => {
        const filtered = players.filter (player =>
            player.in_game_name.toLowerCase().includes(searchTerm.toLowerCase())
        )
        setFilteredPlayers (filtered)
    }, [searchTerm, players])

    const handleFilterChange = (e) => {
        setFilters({
            ...filters,
            [e.target.name]: (e.target.value)
        });
    };

    function capitalize(word) {
        if (!word) return '';
        if (word.charAt(word.length - 1) === "a" && word.charAt(word.length - 2) === "d" && word.charAt(word.length - 3) === "k") {
            return word.charAt(0).toUpperCase() + word.slice (1, word.length - 3).toLowerCase() + word.slice(word.length - 3, word.length).toUpperCase()
        }
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    }

    const handleFilterSubmit = () => {
        Object.keys(filters).forEach((key) => {
            searchParams.set(key, filters[key]);
        });

        navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true, state: {} });
        setShowOverlay(false);
    };

    const handleFilterOverlay = () => {
        setShowOverlay (true)
    }

    return (
        <>
        {showOverlay &&
            <motion.div
            key="filterOverlay"
            className="w-screen h-screen min-h-screen flex justify-center items-center absolute top-0 left-0 z-10 backdrop-blur-lg"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, stiffness: 0 }}
            onClick={() => {setShowOverlay (false)}}>
                <div className="h-5/6 w-5/6 flex flex-col justify-evenly items-center overflow-y-scroll bg-secondary-riot rounded-lg text-white" onClick={(e) => {e.stopPropagation()}}>
                    {/* Filter Name */}
                    <h2 className="text-2xl font-bold mb-4">Filter Options</h2>

                    <div className="flex w-5/6">
                        {/* Render Radio Buttons */}
                        {/* Level Filter */}
                        <div className="w-full mb-4">
                            <label className="text-lg font-semibold border-b-2 border-b-primary-riot">Level</label>
                            <div className="flex flex-col mt-2">
                                {["professional", "semi-professional", "game-changer"].map((option) => (
                                    <label key={option}>
                                        <input
                                            type="radio"
                                            name="level"
                                            value={option}
                                            checked={filters.level === option}
                                            onChange={handleFilterChange}
                                        />
                                        {capitalize(option)}
                                    </label>
                                ))}
                            </div>
                        </div>
                        {/* IGL Filter */}
                        <div className="w-full mb-4">
                            <label className="text-lg font-semibold border-b-2 border-b-primary-riot">IGL</label>
                            <div className="flex flex-col mt-2">
                                {["yes", "no", "any"].map((option) => (
                                    <label key={option}>
                                        <input
                                            type="radio"
                                            name="igl"
                                            value={option}
                                            checked={filters.igl === option}
                                            onChange={handleFilterChange}
                                        />
                                        {capitalize(option)}
                                    </label>
                                ))}
                            </div>
                        </div>
                        {/* Role Filter */}
                        <div className="w-full mb-4">
                            <label className="text-lg font-semibold border-b-2 border-b-primary-riot">Role</label>
                            <div className="flex flex-col mt-2">
                                {["duelist", "initiator", "controller", "sentinel"].map((option) => (
                                    <label key={option}>
                                        <input
                                            type="radio"
                                            name="role"
                                            value={option}
                                            checked={filters.role === option}
                                            onChange={handleFilterChange}
                                        />
                                        {capitalize(option)}
                                    </label>
                                ))}
                            </div>
                        </div>
                        {/* SortBy Filter */}
                        <div className="w-full mb-4">
                            <label className="text-lg font-semibold border-b-2 border-b-primary-riot">Sort By</label>
                            <div className="flex flex-col mt-2">
                                {["name", "attacking-kda", "defending-kda", "kills", "deaths", "assists", "year", "team"].map((option) => (
                                    <label key={option}>
                                        <input
                                            type="radio"
                                            name="sortBy"
                                            value={option}
                                            checked={filters.sortBy === option}
                                            onChange={handleFilterChange}
                                        />
                                        {capitalize(option)}
                                    </label>
                                ))}
                            </div>
                        </div>
                        {/* Sort Order Filter */}
                        <div className="w-full mb-4">
                            <label className="text-lg font-semibold border-b-2 border-b-primary-riot">Sort Order</label>
                            <div className="flex flex-col mt-2">
                                {["ASC", "DESC"].map((option) => (
                                    <label key={option}>
                                        <input
                                            type="radio"
                                            name="sortOrder"
                                            value={option}
                                            checked={filters.sortOrder === option}
                                            onChange={handleFilterChange}
                                        />
                                        {option}
                                    </label>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Submit Button */}
                    <button
                        className="bg-primary-riot h-8 rounded-sm font-Tungsten text-white text-3xl flex justify-center items-center w-1/6 hover:text-secondary-riot outline-1 outline-white outline-offset-2"
                        onClick={handleFilterSubmit}>
                        Submit
                    </button>
                </div>
            </motion.div>}
            <div className="w-11/12 h-15/16 flex flex-col justify-start items-center">
                <div className="flex w-full justify-between items-center">
                    <div className="w-10/12">
                        <input type="text" className="w-full h-10 rounded-sm px-2 bg-white bg-opacity-75 focus:border-2 focus:border-primary-riot focus:outline-none" placeholder="Filter results" value={searchTerm} onChange={(e) => {setSearchTerm (e.target.value)}} />
                    </div>
                    <div className="flex justify-center items-center text-white bg-primary-riot bg-opacity-75 hover:bg-opacity-100 duration-100 rounded-sm h-10 w-1/12 px-2 cursor-pointer hover:border-secondary-riot" onClick={handleFilterOverlay}>
                        <img src={filterIcon} className="h-6" />
                    </div>
                </div>
                <div className="w-full h-full flex justify-between items-center">
                    <div className="w-2/16 h-full flex flex-col justify-start items-center overflow-y-scroll">
                        {!isLoading ? filteredPlayers.map ((player) => (
                            <PlayerElement key={player.player_id + "" + player.home_team_id} player={player} setSelectedPlayer={setSelectedPlayer} />
                        )) : <div className="w-full h-full flex justify-center items-center"><img className="h-1/3" src={loadingAnimation} /></div>}
                    </div>
                    <div className="w-13/16 h-full">
                        {selectedPlayer && <SelectedPlayerElement player={selectedPlayer} />}
                    </div>
                </div>
            </div>
        </>
    )
}