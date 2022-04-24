import {formatSince} from "./lib/tools";


const ModeTitle = ({mode, since}: { mode: string, since: string | undefined }) => {
    return (<div>
        {mode === 'clock_mode' && 'Manual Watering'}
        {mode === 'timer_mode' && 'Timed Watering'}
        {mode === 'wait_mode' && 'Choose a watering mode'}
        &nbsp;
        {since && `since ${formatSince(since, '')}`}
    </div>)
}

export default ModeTitle