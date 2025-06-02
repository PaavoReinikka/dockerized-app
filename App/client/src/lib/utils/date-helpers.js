
export const datesInOrder = (startTime, endTime) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    return start <= end;
};

export const getFormattedDates = (data, time_key = "startTime", value_key = "value") => {
    // Sort by the original UTC time
    const sorted = [...data].sort(
        (a, b) => new Date(a[time_key]) - new Date(b[time_key])
    );

    // Map to Helsinki time and extract values
    const labels = sorted.map(item =>
        new Date(item[time_key]).toLocaleString("fi-FI", {
            timeZone: "Europe/Helsinki",
            year: "numeric",
            month: "numeric",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        })
    );
    const values = sorted.map(item => item[value_key]);

    return { values, labels };
};

export const getTomorrow = () => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    return d.toISOString().slice(0, 10);
}