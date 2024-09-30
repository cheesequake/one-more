import { motion } from "framer-motion"

export default function About () {
    return (
        <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-11/12 h-15/16 border-l flex flex-col justify-center items-center border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25">
        </motion.div>
    )
}