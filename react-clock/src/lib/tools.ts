export function format(value: number) {
    return String(value).padStart(2, '0')
}

export function formatSince(since: string | undefined, defaultValue: string = '--:--:--') {
    if (since) {
        const date = new Date(since);
        return `${format(date.getHours())}:${format(date.getMinutes())}:${format(date.getSeconds())}`;
    } else {
        return defaultValue;
    }
}
