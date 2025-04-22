import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { COOKIE_KEY } from "$env/static/private";


export const actions = {
    retrieveData: async ({ request, params, cookies }) => {
        //console.log(data);
        //console.log(JSON.stringify(request.headers.get("Cookie")));
        //console.log(cookies.getAll());
        //console.log(request.headers.get("Cookie"));
        //console.log(cookies.get(COOKIE_KEY));
        const response = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/data`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Cookie": `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`,
            },
            credentials: "include",
        });
        //console.log(response);
        if (!response.ok) {
            return { success: false, error: "Failed to fetch data" };
        }
        const chartData = await response.json();
        return { success: true, chartData };
    }
};