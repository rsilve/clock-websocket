import {elapsed, formatSince} from "./lib/tools";

interface ModeTitleProps {
    mode: string;
    since?: string;
    timestamp?: string;
    to?: string;
}

const ModeTitle = ({mode, since, timestamp, to}: ModeTitleProps) => {
    return (<div>
        {mode === 'manual_mode' && 'Manual Watering'}
        {mode === 'timer_mode' && 'Timed Watering'}
        {mode === 'wait_mode' && 'Choose a watering mode'}
        &nbsp;
        {since && `since ${formatSince(since, '')}`}
        &nbsp;
        {mode === 'manual_mode' && `elapsed ${elapsed(since, timestamp)}`}
        {mode === 'timer_mode' && `remaining ${elapsed(timestamp, to)}`}
    </div>)
}

export default ModeTitle