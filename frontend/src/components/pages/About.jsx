import { AnimatePresence, motion } from "framer-motion"
import about from "../../assets/about.png"
import onemore from "../../assets/one-more-light.png"

export default function About () {
    return (
        <AnimatePresence>
            <motion.div
            key="about"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-11/12 h-15/16 flex flex-col justify-start items-center border-l border-l-white border-r border-r-white backdrop-blur-lg content bg-slate-100 bg-opacity-25 overflow-y-scroll">
                <img src={about} className="w-2/3" />
                <div className="p-2 text-white">
                    <img src={onemore} className="h-6 inline" /> is a LLM-powered digital assistant which analyses the vast datasource of the many games played in the history of Valorant, and utilises the power of <a href="https://aws.amazon.com/bedrock/" className="font-medium">Amazon Bedrock</a> to answer questions effectively. It is my (<a href="https://github.com/cheesequake" className="font-medium">Cheesequake's</a>) submission for the <a href="https://vcthackathon.devpost.com/" className="font-medium">VCT Hackathon: Esports Manager Challenge</a>.<br /><br />
                    Under the hood, it is a Text-to-SQL and SQL-to-NL application. Looking at the sample prompts, this seemed like a very good option. This application is hosted on AWS EC2 instance, and the database has been prepared in AWS RDS. This is completely a solo project.<br />
                    Currently, it leverages the combined power of Mistral's Large model for SQL generation, and Llama 3 for natural language processing. Due to the abstraction from Bedrock, we can try out various models too. To know more about the code and the structure, please visit this private repository (<a href="" className="font-medium">here</a>).<br /><br />
                    This application has been built on VCT Champions 2023 theme, with Patch 7.02 Homescreen, also inspired from the music video of <a href="https://www.youtube.com/watch?v=CdZN8PI3MqM" className="font-medium">Ticking Away ft. Grabbitz & bbno$</a>. The music video narrates a story of a young boy aspiring to be a professional Valorant player, finally achieving his dream at the end. This video has been a huge source of inspiration for me, and my favourite player Demon1 winning Champions 2023 further solidified my love for Valorant and gave me a motivation to be the best at what I do.
                </div>
            </motion.div>
        </AnimatePresence>
    )
}