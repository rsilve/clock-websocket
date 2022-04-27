import {elapsed, formatSince} from "./lib/tools";

interface ModeReportProps {
    mode: string;
    since?: string;
    timestamp?: string;
    to?: string;
}

const TimeStamp = ({timestamp}: {timestamp: string}) => {
    return <span className="timestamp">{timestamp}</span>;
};

const ModeReport = ({mode, since, timestamp, to}: ModeReportProps) => {
    return (<div className="mode-report">
        {mode === 'manual_mode' && 'Manual Watering'}
        {mode === 'timer_mode' && 'Timed Watering'}
        {mode === 'wait_mode' && 'Choose a watering mode'}
        <br/>
        {since && `since ${formatSince(since, '')}`}
        <br/>
        {mode === 'manual_mode' && `elapsed ${elapsed(since, timestamp)}`}
        {mode === 'timer_mode' && `remaining ${elapsed(timestamp, to)}`}
    </div>)
}

export default ModeReport;
