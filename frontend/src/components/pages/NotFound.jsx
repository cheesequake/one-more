import { AnimatePresence, motion } from "framer-motion";
import widejoy from "../../assets/widejoy.jpg"

export default function NotFound () {
    return (
        <AnimatePresence>
            <motion.div
            key="not-found"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-11/12 h-15/16 flex flex-col justify-center items-center border-l border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25 font-Tungsten text-6xl text-white">
                <img src={widejoy} className="w-full" />
                YOU ARE AT THE WRONG PLACE!
            </motion.div>
        </AnimatePresence>
    )
}