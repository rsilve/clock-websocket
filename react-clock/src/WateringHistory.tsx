import {formatSince} from "./lib/tools";

interface WateringHistoryProps {
    history: { since: string, mode: string, timestamp: string }[];
}

interface WateringHistoryItemProps {
    timestamp: string;
    since: string;
    mode: string;
    duration: number;
}

function prepareHistory(history: { since: string, mode: string, timestamp: string }[]) {
    const histogram = history.map(value => {
        const end = new Date(value.timestamp);
        const start = new Date(value.since);
        const duration = end.getTime() - start.getTime();
        return {...value, duration};
    })
    const max = histogram.reduce((acc, curr) => {
        return Math.max(acc, curr.duration);
    }, 1);
    return histogram.map(value => {
        return {...value, duration: value.duration / max};
    });

}

const WateringHistoryItem = ({ timestamp, since, mode, duration }: WateringHistoryItemProps) => {
    const style = {width: `${duration*100}%`};
    return (<li style={style} className={mode}>{formatSince(since)} - {formatSince(timestamp)}</li>)
}

const WateringHistory = ({history}: WateringHistoryProps) => {
    const normalizedHistory = prepareHistory(history);
    return (<ul className="history-graph">
        {normalizedHistory.map((item: WateringHistoryItemProps) => <WateringHistoryItem
            key={item.since} {...item}/>)}
    </ul>)
}


export default WateringHistory;