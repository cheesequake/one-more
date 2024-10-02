import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { BrowserRouter } from 'react-router-dom'
import { OptionsContextProvider } from './contexts/OptionsContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <OptionsContextProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </OptionsContextProvider>
  </StrictMode>,
)
