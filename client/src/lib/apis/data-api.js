import { PUBLIC_API_URL } from "$env/static/public";

const readData = async () => {
    const response = await fetch(`${PUBLIC_API_URL}/api/data`, {
        headers: {
        "Content-Type": "application/json",
        },
        method: "GET",
        credentials: "include", // Include cookies in the request
    });
    return await response.json();
};

const readPublicData = async () => {
    const response = await fetch(`${PUBLIC_API_URL}/api/public/data`, {
        headers: {
        "Content-Type": "application/json",
        },
        method: "GET",
    });
    return await response.json();
};

export { readData, readPublicData };
