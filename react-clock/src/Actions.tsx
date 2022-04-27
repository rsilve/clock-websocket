const stopUrl = 'http://localhost:8080/stop'
const clockUrl = 'http://localhost:8080/manual'
const timerUrl = 'http://localhost:8080/timer'


const Actions = ({mode}: { mode: string }) => {
    const manual_mode = async () => {
        await fetch(clockUrl)
    }
    const timer_mode = async () => {
        await fetch(timerUrl)
    }
    const stop = async () => {
        await fetch(stopUrl)
    }
    return (<>
        {mode === 'wait_mode' && <button onClick={manual_mode}>Manual watering</button>}
        {mode === 'wait_mode' && <button onClick={timer_mode}>Timed watering</button>}
        {mode !== 'wait_mode' && <button onClick={stop}>Stop</button>}
    </>)
}

export default Actions;