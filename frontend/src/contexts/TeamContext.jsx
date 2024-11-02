import { createContext, useReducer } from "react";

export const TeamContext = createContext ()

export const teamReducer = (state, action) => {
    switch (action.type) {
        case 'SET':
            return { ...state, team: action.payload }
        default:
            return state
    }
}

export const TeamContextProvider = ({ children }) => {
    const [state, teamDispatch] = useReducer (teamReducer, {
        team: []
    })

    return (
        <TeamContext.Provider value={{...state, teamDispatch}}>
            { children }
        </TeamContext.Provider>
    )
}