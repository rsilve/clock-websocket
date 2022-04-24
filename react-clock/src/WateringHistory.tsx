import {useEffect, useState} from "react";
import {formatSince} from "./lib/tools";

function formatMode(mode: string) {
    switch (mode) {
        case "timer_mode":
            return "Timed";
        case "clock_mode":
            return "Manual";
        default:
            return "Unknown";
    }
}

const WateringHistory = ({mode}: { mode: string }) => {
    const [history, setHistory] = useState([])
    useEffect(() => {
        if (mode === "wait_mode") {
            fetch("http://localhost:8080/history")
                .then(res => res.json())
                .then(data => {
                    setHistory(data)
                })
        }
    }, [mode]);
    return (<ul>
        {history.map((item: { since: string, mode: string, timestamp: string }) => <li
            key={item.since}>{formatMode(item.mode)} from {formatSince(item.since)} to {formatSince(item.timestamp)}</li>)}
    </ul>)
}


export default WateringHistory;