import logo from './logo.svg'
import './App.css'
import useWebSocket from "react-use-websocket";

function format(value: number) {
    return String(value).padStart(2, '0')
}

function App() {
    const {lastMessage} = useWebSocket('ws://localhost:8001');
    let hours = "--";
    let minutes = "--";
    let seconds = "--";
    if (lastMessage?.data) {
        const timestamp = new Date(lastMessage.data)
        hours = format(timestamp.getHours());
        minutes = format(timestamp.getMinutes());
        seconds = format(timestamp.getSeconds());
    }

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
