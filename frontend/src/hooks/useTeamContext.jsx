import { useContext } from "react"
import { TeamContext } from "../contexts/TeamContext"

export const useTeamContext = () => {
    const context = useContext (TeamContext)

    if (!context) {
        throw Error ('useContext must be used inside a provider')
    }

    return context
}