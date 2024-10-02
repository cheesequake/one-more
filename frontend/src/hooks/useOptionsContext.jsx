import { useContext } from "react"
import { OptionsContext } from "../contexts/OptionsContext"

export const useOptionsContext = () => {
    const context = useContext (OptionsContext)

    if (!context) {
        throw Error ('useContext must be used inside a provider')
    }

    return context
}