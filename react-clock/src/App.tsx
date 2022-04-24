import logo from './logo.svg'
import './App.css'
import useWebSocket from "react-use-websocket";
import {useEffect, useState} from "react";

const SOCKET_URL = 'ws://localhost:8080/ws'
const INITIAL_VALUE = "--";

function format(value: number) {
    return String(value).padStart(2, '0')
}

function updateValue(message: string | undefined, setter: (value: string) => void, extract: (date: Date) => number) {
    if (message) {
        const timestamp = new Date(message)
        setter(format(extract(timestamp)));
    } else {
        setter(INITIAL_VALUE)
    }
}

function App() {
    const {lastMessage} = useWebSocket(SOCKET_URL, {
        shouldReconnect: (_ ) => true,
            reconnectAttempts: 10,
            reconnectInterval: 3000,
    });
    const [hours, setHours] = useState(INITIAL_VALUE);
    const [minutes, setMinutes] = useState(INITIAL_VALUE);
    const [seconds, setSeconds] = useState(INITIAL_VALUE);
    useEffect(() => {
        updateValue(lastMessage?.data, setHours, (date: Date) => date.getHours());
        updateValue(lastMessage?.data, setMinutes, (date: Date) => date.getMinutes());
        updateValue(lastMessage?.data, setSeconds, (date: Date) => date.getSeconds());
    }, [lastMessage]);

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <div className="clock">
                    {hours}:{minutes}:{seconds}
                </div>

            </header>
        </div>
    )
}

export default App
