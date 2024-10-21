export default function StatKeyValueElement ({ stat, value }) {
    return (
        <div className="flex">
            <div className="font-medium">
                {stat}
            </div>
            <div className="ml-2">
                {value}
            </div>
        </div>
    )
}