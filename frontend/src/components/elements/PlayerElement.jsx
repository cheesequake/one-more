export default function PlayerElement ({ player, setSelectedPlayer }) {
    return (
        <div className="w-full flex justify-center items-center p-1 border-2 border-primary-riot rounded-sm mt-2 bg-secondary-riot text-primary-riot bg-opacity-75 hover:bg-opacity-100 cursor-pointer hover:text-white" onClick={() => {setSelectedPlayer (player)}} >
            {player.in_game_name}
        </div>
    )
}