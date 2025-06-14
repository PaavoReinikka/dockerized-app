// export const load = async ({ locals }) => {
//     return locals;
//   };
import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";

export const load = async ({ locals, fetch }) => {
    const res = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/public/data`, {
        headers: {
            'Content-Type': 'application/json',
        },
    });
    if (!res.ok) {
        throw new Error(`Failed to fetch data: ${res.statusText}`);
    }
    const prices = await res.json();
    // sort prices by startTime (just in case)
    prices.sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
    return {
        prices,
        user: locals.user,
    };
};