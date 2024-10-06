export default function TeamElement ({ team }) {
    return (
        <div className="backdrop-blur-lg content py-1 bg-slate-100 bg-opacity-25 hover:bg-opacity-50 duration-100 flex flex-col justify-between items-center text-white w-40 h-32 m-2">
            <div className="my-4">
                <img src={team.team_logo_url} className="h-16" />
            </div>
            <div className="cursor-default w-full flex justify-center items-center font-light bg-slate-100 bg-opacity-25">
                {team.team_name}
            </div>
        </div>
    )
}