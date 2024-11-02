import { createContext, useReducer } from "react";

export const MessagesContext = createContext ()

export const messagesReducer = (state, action) => {
    switch (action.type) {
        case 'SET':
            return { ...state, messages: action.payload }
        default:
            return state
    }
}

export const MessagesContextProvider = ({ children }) => {
    const [state, messagesDispatch] = useReducer (messagesReducer, {
        messages: []
    })

    return (
        <MessagesContext.Provider value={{...state, messagesDispatch}}>
            { children }
        </MessagesContext.Provider>
    )
}