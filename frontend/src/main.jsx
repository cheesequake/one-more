import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { BrowserRouter } from 'react-router-dom'
import { OptionsContextProvider } from './contexts/OptionsContext.jsx'
import { TeamContextProvider } from './contexts/TeamContext.jsx'
import { MessagesContextProvider } from './contexts/MessagesContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <MessagesContextProvider>
        <TeamContextProvider>
          <OptionsContextProvider>
              <App />
          </OptionsContextProvider>
        </TeamContextProvider>
      </MessagesContextProvider>
    </BrowserRouter>
  </StrictMode>,
)
