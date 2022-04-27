import {formatSince} from "./lib/tools";
import useWebSocket from "react-use-websocket";
import {useContext, useEffect, useState} from "react";
import AppDispatch from "./AppDispatch";

const SOCKET_URL = 'ws://localhost:8080/ws'

const Clock = () => {
    const dispatch = useContext(AppDispatch)
    const [timestamp, setTimestamp] = useState(undefined as string | undefined)
    const {lastJsonMessage} = useWebSocket(SOCKET_URL, {
        shouldReconnect: (_) => true,
        reconnectAttempts: 1000,
        reconnectInterval: 3000,
    });

    useEffect(() => {
        if (lastJsonMessage && dispatch) {
            dispatch({type: 'ws', payload: lastJsonMessage})

            if (lastJsonMessage.timestamp !== timestamp) {
                setTimestamp(lastJsonMessage.timestamp)
            }
        }
    }, [lastJsonMessage]);

    return (<div className="clock">
        {formatSince(timestamp)}
    </div>)
}

export default Clock