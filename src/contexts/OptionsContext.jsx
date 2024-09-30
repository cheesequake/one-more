import { createContext, useReducer } from "react";

export const OptionsContext = createContext ()

export const optionsReducer = (state, action) => {
    switch (action.type) {
        case 'SET':
            return { ...state, option: action.payload }
        default:
            return state
    }
}

export const OptionsContextProvider = ({ children }) => {
    const [state, dispatch] = useReducer (optionsReducer, {
        option: 0
    })

    return (
        <OptionsContext.Provider value={{...state, dispatch}}>
            { children }
        </OptionsContext.Provider>
    )
}