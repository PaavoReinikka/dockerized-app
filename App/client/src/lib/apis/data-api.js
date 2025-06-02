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
    try {
        const response = await fetch(`${PUBLIC_API_URL}/api/public/data`, {
            headers: {
            "Content-Type": "application/json",
            },
            method: "GET",
        });
        if (!response.ok) {
            console.error(`API error! status: ${response.status}`);
            return [];
        } 
        
        return await response.json(); 
    } catch (error) {
        console.error('Failed to fetch public data:', error);
		return [];
    }  
};

const readPriceRange = async (startTime, endTime) => {
    const response = await fetch(`${PUBLIC_API_URL}/api/price/range`, {
        headers: {
        "Content-Type": "application/json",
        },
        credentials: "include",
        method: "POST",
        body: JSON.stringify({
            startTime,
            endTime,
        }),
    });
    return await response.json();
}

export { readData, readPublicData, readPriceRange };
