import axios from "axios"
import PlayerElement from "../elements/PlayerElement"
import loadingAnimation from "../../assets/LoadingAnimation.gif"
import { useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import { AnimatePresence, motion } from "framer-motion"
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
        level: searchParams.get('level') || 'Professional',
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
        const allowedLevels = ["Professional", "Semi-Professional", "Game-Changer"]
        const allowedIgls = ["yes", "no", "any"]
        const allowedRoles = ["duelist", "initiator", "controller", "sentinel"]
        const allowedSortBy = ["name", "attacking-kda", "defending-kda", "kills", "deaths", "assists", "year", "team"]
        const allowedSortOrder = ["ASC", "DESC"]
        let updated = false

        setIsLoading (true)
        const getData = async () => {
            try {
                const params = {
                    level: level,
                    igl: igl,
                    role: role,
                    sortBy: sortBy,
                    sortOrder: sortOrder
                }

                const playerResponse = await axios.get (import.meta.env.VITE_BACKEND_URL+"players", { params })

                setPlayers (playerResponse.data)

                setIsLoading (false)
            }
            catch (error) {
                console.log (error)
            }
        }

        if (!level || !allowedLevels.includes(level)) {
            searchParams.set('level', 'Professional')
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
        <AnimatePresence>
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
                                {["Professional", "Semi-Professional", "Game-Changer"].map((option) => (
                                    <label key={option}>
                                        <input
                                            type="radio"
                                            name="level"
                                            value={option}
                                            checked={filters.level === option}
                                            onChange={handleFilterChange}
                                        />
                                        {option}
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
                <div className="flex h-2/16 w-full justify-between items-center">
                    <div className="w-10/12">
                        <input type="text" className="w-full h-10 rounded-sm px-2 bg-white bg-opacity-75 focus:border-2 focus:border-primary-riot focus:outline-none" placeholder="Filter results" value={searchTerm} onChange={(e) => {setSearchTerm (e.target.value)}} />
                    </div>
                    <div className="flex justify-center items-center text-white bg-primary-riot bg-opacity-75 hover:bg-opacity-100 duration-100 rounded-sm h-10 w-1/12 px-2 cursor-pointer hover:border-secondary-riot" onClick={handleFilterOverlay}>
                        <img src={filterIcon} className="h-6" />
                    </div>
                </div>
                <div className="w-full h-14/16 flex justify-between items-center">
                    <div className="w-2/16 h-full flex flex-col justify-start items-center overflow-y-scroll">
                        {!isLoading ? filteredPlayers.map ((player) => (
                            <PlayerElement key={player.player_id + "" + player.team_acronym} player={player} setSelectedPlayer={setSelectedPlayer} />
                        )) : <div className="w-full flex justify-center items-center"><img className="h-1/3" src={loadingAnimation} /></div>}
                    </div>
                    <div className="w-13/16 h-full">
                        {selectedPlayer && <SelectedPlayerElement player={selectedPlayer} />}
                    </div>
                </div>
            </div>
        </AnimatePresence>
    )
}