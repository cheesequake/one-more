import { useContext } from "react"
import { MessagesContext } from "../contexts/MessagesContext"

export const useMessagesContext = () => {
    const context = useContext (MessagesContext)

    if (!context) {
        throw Error ('useContext must be used inside a provider')
    }

    return context
}