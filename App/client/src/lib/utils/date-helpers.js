
export const datesInOrder = (startTime, endTime) => {
    // This function checks if the start date is before or equal to the end date.
    const start = new Date(startTime);
    const end = new Date(endTime);
    return start <= end;
};

export const datesCloseEnough = (startTime, endTime) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const sixMonthsAgo = new Date(end);
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
    if (start < sixMonthsAgo) {
        return false; // start date is more than 6 months before end date
    }
    return true;
};

export const getFormattedDates = (data, time_key = "startTime", value_key = "value") => {
    // This function takes an array of objects and 
    // returns formatted and sorted dates and values.
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
    // This function returns tomorrow's date in ISO format (YYYY-MM-DD)
    const d = new Date();
    d.setDate(d.getDate() + 1);
    d.setHours(d.getHours() + 3);
    return d.toISOString().slice(0, 10);
}

export const isTodayHelsinki = (dateStr) => {
    // This function checks if the given date string is today in Helsinki time
        const d = new Date(dateStr);
        const today = new Date().toLocaleDateString('fi-FI', { timeZone: 'Europe/Helsinki' });
        const dDate = d.toLocaleDateString('fi-FI', { timeZone: 'Europe/Helsinki' });
        return dDate === today;
    }