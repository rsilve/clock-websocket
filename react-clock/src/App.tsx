import logo from './logo.svg'
import './App.css'
import Clock from "./Clock";
import Actions from "./Actions";
import useWebSocket from "react-use-websocket";
import {useEffect, useState} from "react";
import ModeReport from "./ModeReport";
import WateringHistory from "./WateringHistory";

const SOCKET_URL = 'ws://localhost:8080/ws'

function App() {
    const [mode, setMode] = useState('wait_mode')
    const [timestamp, setTimestamp] = useState(undefined as string | undefined)
    const [since, setSince] = useState(undefined as string | undefined)
    const [to, setTo] = useState(undefined as string | undefined)
    const [history, setHistory] = useState([])
    const {lastJsonMessage} = useWebSocket(SOCKET_URL, {
        shouldReconnect: (_) => true,
        reconnectAttempts: 1000,
        reconnectInterval: 3000,
    });

    useEffect(() => {
        if (lastJsonMessage) {
            if (lastJsonMessage.mode !== mode) {
                setMode(lastJsonMessage.mode)
            }
            if (lastJsonMessage.timestamp !== timestamp) {
                setTimestamp(lastJsonMessage.timestamp)
            }
            if (lastJsonMessage.since !== since) {
                setSince(lastJsonMessage.since)
            }
            if (lastJsonMessage.to !== to) {
                setTo(lastJsonMessage.to)
            }
        }
    }, [lastJsonMessage]);

    useEffect(() => {
        fetch("http://localhost:8080/history")
            .then(res => res.json())
            .then(data => {
                setHistory(data)
            })
    }, [mode]);
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
            </header>
            <div className="App-body">
                <Clock timestamp={timestamp}/>
                <ModeReport mode={mode} since={since} timestamp={timestamp} to={to}/>
            </div>
            <div className="App-actions">
                <Actions mode={mode}/>
            </div>
            <div className="App-history">
                <WateringHistory history={history}/>
            </div>

        </div>
    )
}

export default App
