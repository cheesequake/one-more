import axios from "axios"
import { AnimatePresence, motion } from "framer-motion"
import { useEffect, useRef, useState } from "react"
import Markdown from 'react-markdown'
import { useTeamContext } from '../../hooks/useTeamContext'
import { useMessagesContext } from '../../hooks/useMessagesContext'

export default function Play () {
    const [animating, setAnimating] = useState (true)
    const [lock, setLock] = useState (false)
    const [query, setQuery] = useState ("")
    const { team, teamDispatch } = useTeamContext ()
    const { messages, messagesDispatch } = useMessagesContext ()
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

        let newMessages = [...messages, { sender: 'user', text: query }]
        messagesDispatch ({
            type: "SET",
            payload: newMessages
        });

        await axios.post (import.meta.env.VITE_BACKEND_URL+"generate_response", {query: query, team: team})
        .then (response => {
            if (response.data.output) {
                messagesDispatch({
                    type: "SET",
                    payload: [
                        ...newMessages,
                        { sender: 'AI', text: response.data.output }
                    ]
                });
                response.data.data = JSON.parse(response.data.data);

                if (Array.isArray(response.data.data) && response.data.data.length <= 5) {
                    // Define the roles and initialize with null if `team` is not yet set
                    const roles = { Duelist: null, Initiator: null, Controller: null, Sentinel: null, IGL: null };

                    // Step 1: Process the incoming players and assign them to their roles in `roles`
                    response.data.data.forEach(player => {
                        if (player.in_game_name && (player.agent_name || player.most_played_agent)) {
                            if ((player.assigned_role === 'duelist' || player.role === 'duelist') && !roles.Duelist) {
                                roles.Duelist = player;
                            } else if ((player.assigned_role === 'initiator' || player.role === 'initiator') && !roles.Initiator) {
                                roles.Initiator = player;
                            } else if ((player.assigned_role === 'controller' || player.role === 'controller') && !roles.Controller) {
                                roles.Controller = player;
                            } else if ((player.assigned_role === 'sentinel' || player.role === 'sentinel') && !roles.Sentinel) {
                                roles.Sentinel = player;
                            } else if (player.in_game_leader === 1 && !roles.IGL) {
                                roles.IGL = player;
                            }
                        }
                    });
                
                    // Step 2: Initialize or update `team` with the roles data
                    let updatedTeam;
                    if (!team || team.length === 0) {
                        // Initialize `team` with empty slots for all roles if it doesn't exist
                        updatedTeam = [
                            roles.Duelist || { assigned_role: 'duelist' },
                            roles.Initiator || { assigned_role: 'initiator' },
                            roles.Controller || { assigned_role: 'controller' },
                            roles.Sentinel || { assigned_role: 'sentinel' },
                            roles.IGL || { in_game_leader: 1 }
                        ];
                    } else {
                        updatedTeam = team.map(player => {
                            if (player.assigned_role === 'duelist' || player.role === 'duelist') {
                                return roles.Duelist || player;
                            } else if (player.assigned_role === 'initiator' || player.role === 'initiator') {
                                return roles.Initiator || player;
                            } else if (player.assigned_role === 'controller' || player.role === 'controller') {
                                return roles.Controller || player;
                            } else if (player.assigned_role === 'sentinel' || player.role === 'sentinel') {
                                return roles.Sentinel || player;
                            } else if (player.in_game_leader === 1) {
                                return roles.IGL || player;
                            }
                            return player;
                        });
                    }

                    // Dispatch the updated team
                    teamDispatch({ type: 'SET', payload: updatedTeam });
                }
                

                setLock (false)
            }
            else {
                messagesDispatch({
                    type: "SET",
                    payload: [
                        ...newMessages,
                        { sender: 'AI', text: "Sorry, I think I'll need a Tech Pause." }
                    ]
                });
                setLock (false)
            }
        })
        .catch (() => {
            messagesDispatch({
                type: "SET",
                payload: [
                    ...newMessages,
                    { sender: 'AI', text: "Sorry, I think I'll need a Tech Pause." }
                ]
            });
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
            className="w-11/12 h-15/16 border-l flex flex-col justify-center items-start border-l-white border-r border-r-white backdrop-blur-lg content bg-secondary-riot bg-opacity-25">
                {!animating &&
                <>
                    <div className="w-15/16 min-h-5/6 max-h-5/6 overflow-y-scroll flex flex-col">
                        {messages.map ((message, index) => (
                            <motion.div key={index} className={`p-2 mb-2 text-white break-words self-start max-w-3xl rounded-tr-xl rounded-br-xl rounded-bl-xl flex`}
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