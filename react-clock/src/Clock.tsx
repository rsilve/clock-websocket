import {formatSince} from "./lib/tools";

const Clock = ({timestamp}: { timestamp: string | undefined }) => {

    return (<div className="clock">
        {formatSince(timestamp)}
    </div>)
}

export default Clock