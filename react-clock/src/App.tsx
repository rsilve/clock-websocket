import logo from './logo.svg'
import './App.css'
import Clock from "./Clock";
import Actions from "./Actions";
import {useReducer} from "react";
import ModeReport from "./ModeReport";
import WateringHistory from "./WateringHistory";
import reducer from "./lib/reducer";
import AppDispatch from './AppDispatch';


const initialState = {mode: 'wait_mode'};

function App() {

    const [state, dispatch] = useReducer(reducer, initialState);

    return (
        <AppDispatch.Provider value={dispatch}>
            <div className="App">
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                </header>
                <div className="App-body">
                    <Clock />
                    <ModeReport mode={state.mode} since={state.since} timestamp={state.timestamp} to={state.to}/>
                </div>
                <div className="App-actions">
                    <Actions mode={state.mode}/>
                </div>
                <div className="App-history">
                    <WateringHistory mode={state.mode}/>
                </div>
            </div>
        </AppDispatch.Provider>
    )
}

export default App
