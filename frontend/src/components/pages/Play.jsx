import axios from "axios"
import { AnimatePresence, motion } from "framer-motion"
import { useEffect, useRef, useState } from "react"
import Markdown from 'react-markdown'

export default function Play () {
    const [animating, setAnimating] = useState (true)
    const [lock, setLock] = useState (false)
    const [query, setQuery] = useState ("")
    const [messages, setMessages] = useState ([])
    const messagesEndRef = useRef (null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
      }, [messages]);

    useEffect (() => {
        const timer = setTimeout (() => {
            setAnimating (false)
        }, 1000)

        return () => clearTimeout (timer)
    }, [])

    const handleQuery = async () => {
        setLock (true)
        if (!query.trim()) {
            setLock (false)
            return;
        }

        const newMessages = [...messages, { sender: 'user', text: query }]
        setMessages (newMessages)

        await axios.post (import.meta.env.VITE_BACKEND_URL+"generate_response", {query: query})
        .then (response => {
            if (response.data) {
                setMessages ((prevMessages) => [
                    ...prevMessages,
                    { sender: 'server', text: response.data }
                ])
                setLock (false)
            }
            else {
                setMessages ((prevMessages) => [
                    ...prevMessages,
                    { sender: 'server', text: "Sorry, I think I'll need a Tech Pause." }
                ])
                setLock (false)
            }
        })
        .catch (() => {
            setMessages ((prevMessages) => [
                ...prevMessages,
                { sender: 'server', text: "Sorry, I think I'll need a Tech Pause." }
            ])
            setLock (false)
        })

        scrollTo
        setQuery ('')
    }

    return (
        <AnimatePresence>
            <motion.div
            key="play"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, stiffness: 0 }}
            className="w-11/12 h-15/16 border-l flex flex-col justify-center items-center border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25">
                {!animating &&
                <>
                    <div className="w-15/16 min-h-5/6 max-h-5/6 overflow-y-scroll flex flex-col">
                        {messages.map ((message, index) => (
                            <motion.div key={index} className={`p-2 mb-2 text-white break-words self-start max-w-2xl rounded-tr-xl rounded-br-xl rounded-bl-xl flex`}
                            initial={{ scale: 0.5, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                            >
                                {message.sender === 'user' ? (
                                    <span className="text-cyan-300 inline">User:</span>
                                ) : (
                                    <span className="text-red-400 inline">Bot:</span>
                                )}
                                <Markdown className="ml-4">
                                {message.text}
                                </Markdown>
                            </motion.div>
                        ))}
                        <div ref={messagesEndRef} className="min-h-2 max-h-2" />
                    </div>
                    <div className="w-full flex justify-around items-center">
                        <input type="text" className="w-9/12 p-1 h-8" placeholder="Enter a query" value={query} onChange={(e) => { setQuery (e.target.value) }} />
                        <button className={`w-2/12 h-8 rounded-sm font-Tungsten text-3xl flex justify-center items-center ${lock ? 'bg-gray-400 text-gray-300 cursor-not-allowed' : 'bg-primary-riot text-white hover:text-secondary-riot'}`}  onClick={handleQuery} disabled={lock} >
                            ASK
                        </button>
                    </div>
                </>
                }
            </motion.div>
        </AnimatePresence>
    )
}