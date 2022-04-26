export function format(value: number) {
    return String(value).padStart(2, '0')
}

export function elapsed(start?: string, end?: string,) {
    if (!start || !end) {
        return '--:--';
    }
    const startDate = new Date(start)
    const endDate = new Date(end)
    let diff = endDate.getTime() - startDate.getTime()
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const minutes = Math.floor(diff / (1000 * 60)) - hours * 60
    const seconds = Math.floor(diff / 1000) - hours * 60 * 60 - minutes * 60
    return `${format(hours)}:${format(minutes)}:${format(seconds)}`;
}

export function formatSince(since?: string, defaultValue: string = '--:--:--') {
    if (since) {
        const date = new Date(since);
        return `${format(date.getHours())}:${format(date.getMinutes())}:${format(date.getSeconds())}`;
    } else {
        return defaultValue;
    }
}
