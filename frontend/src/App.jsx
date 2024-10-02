import { useState, useRef } from "react"
import videoBG from "./assets/VideoBackground.mp4"
import Navbar from "./components/Navbar"
import Sidebar from "./components/Sidebar"
import { Navigate, Route, Routes } from "react-router-dom"
import About from "./components/pages/About"
import Play from "./components/pages/Play"
import Players from "./components/pages/Players"
import Teams from "./components/pages/Teams"
import NotFound from "./components/pages/NotFound"
import { AnimatePresence } from "framer-motion"

function App() {
  const videoRef = useRef (null)
  const [muted, setMuted] = useState (true)

  return (
    <AnimatePresence>
      <video ref={videoRef} src={videoBG} autoPlay loop muted={muted} className="h-full w-full object-cover absolute top-0 left-0 -z-10" />
      <Navbar muted={muted} setMuted={setMuted} />
      <div className="w-full min-h-90vh h-90vh flex justify-center items-start">
        <Sidebar />
        <div className="w-4/5 h-full flex justify-center items-center font-FF-Mark font-normal">
            <Routes>
              <Route path="/" element={null} />
              <Route path="/about" element={<About />} />
              <Route path="/play" element={<Play />} />
              <Route path="/players" element={<Players />} />
              <Route path="/teams" element={<Teams />} />

              <Route path="/not-found" element={<NotFound />} />
              <Route path="*" element={<Navigate to="/not-found" />} />
            </Routes>
        </div>
      </div>
    </AnimatePresence>
  )
}

export default App
