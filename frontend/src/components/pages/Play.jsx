import axios from "axios"
import { motion } from "framer-motion"
import { useEffect, useRef, useState } from "react"

export default function Play () {
    const [animating, setAnimating] = useState (true)
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
        if (!query.trim()) return;

        const newMessages = [...messages, { sender: 'user', text: query }]
        setMessages (newMessages)

        await axios.get ("http://localhost:8080/message")
        .then (response => {
            setMessages ((prevMessages) => [
                ...prevMessages,
                { sender: 'server', text: response.data }
            ])
        })
        .catch (() => {
            setMessages ((prevMessages) => [
                ...prevMessages,
                { sender: 'server', text: response.data }
            ])
        })

        scrollTo
        setQuery ('')
    }

    return (
        <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.75, stiffness: 0 }}
        className="w-11/12 h-15/16 border-l flex flex-col justify-center items-center border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25">
            {!animating &&
            <>
                <div className="w-15/16 min-h-5/6 max-h-5/6 overflow-y-scroll flex flex-col">
                    {messages.map ((message, index) => (
                        <motion.div key={index} className={`p-2 rounded-md max-w-96 bg-white break-words ${message.sender === 'user' ? 'self-end' : 'self-start'}`}
                        initial={{ scale: 0.5, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                        >
                            {message.text}
                        </motion.div>
                    ))}
                    <div ref={messagesEndRef} className="min-h-2 max-h-2" />
                </div>
                <div className="w-full flex justify-around items-center">
                    <input type="text" className="w-9/12 p-1 h-8" placeholder="Enter a query" onChange={(e) => { setQuery (e.target.value) }} />
                    <button className="w-2/12 bg-primary-riot h-8 rounded-sm font-Tungsten text-white text-3xl flex justify-center items-center" onClick={handleQuery}>
                        ASK
                    </button>
                </div>
            </>
            }
        </motion.div>
    )
}