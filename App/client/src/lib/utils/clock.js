import { readable } from 'svelte/store'

const formatDate = (date) => {
    return date.toString().replace(/\s*\(.*?\)\s*$/, "");
}

export const clockStore = (options={}) => {
    const initial = new Date()

    // return a readable store
    return readable(formatDate(initial), set => {
        const update = () => set(formatDate(new Date()))
        const interval = setInterval(update, options.interval || 1000)
        return () => clearInterval(interval)
    })
}