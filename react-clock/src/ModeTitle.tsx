import {elapsed, formatSince, remain} from "./lib/tools";

interface ModeTitleProps {
    mode: string;
    since?: string;
    timestamp?: string;
}

const ModeTitle = ({mode, since, timestamp}: ModeTitleProps) => {
    return (<div>
        {mode === 'manual_mode' && 'Manual Watering'}
        {mode === 'timer_mode' && 'Timed Watering'}
        {mode === 'wait_mode' && 'Choose a watering mode'}
        &nbsp;
        {since && `since ${formatSince(since, '')}`}
        &nbsp;
        {mode === 'manual_mode' && `elapsed ${elapsed(since, timestamp)}`}
        {mode === 'timer_mode' && `remaining ${remain(since, timestamp)}`}
    </div>)
}

export default ModeTitle