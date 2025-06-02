export const getStats = (values) => {
    if (!values || values.length === 0) return {};

    const n = values.length;
    const mean = values.reduce((a, b) => a + b, 0) / n;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
    const std = Math.sqrt(variance);
    const median = values.sort((a, b) => a - b)[Math.floor(n / 2)];

    //round to 1 decimal places
    return {
        mean: Math.round(mean * 10) / 10,
        min: Math.round(min * 10) / 10,
        max: Math.round(max * 10) / 10,
        variance: Math.round(variance * 10) / 10,
        std: Math.round(std * 10) / 10,
        median: Math.round(median * 10) / 10,
        count: n,
    };
}