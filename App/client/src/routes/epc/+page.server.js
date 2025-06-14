import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { datesInOrder, getFormattedDates, datesCloseEnough } from '$lib/utils/date-helpers.js';
import { fail } from "@sveltejs/kit";
import { COOKIE_KEY } from "$env/static/private";
import { error, redirect } from "@sveltejs/kit";

export const load = async ({ locals, url }) => {
  if (!locals.user) {
    // Not logged in, redirect to login
    throw redirect(303, `/auth/login`);
  }
  return {};
};

export const actions = {
    getCombinedRange: async ({ request, cookies }) => {
        const fdata = await request.formData();
        const data = Object.fromEntries(fdata);

        if (!data.startTime || !data.endTime) {
            return fail(400, { error: "Start and end dates are required." });
        } else if (!datesInOrder(data.startTime, data.endTime)) {
            return fail(400, { error: "Start date must come before end date." });
        } else if (!datesCloseEnough(data.startTime, data.endTime)) {
            return fail(400, { error: "The date range must be within the last 6 months." });
        }

        try {
            // Fetch datasets in parallel
            const [prodRes, consRes, priceRes] = await Promise.all([
                fetch(`${PUBLIC_INTERNAL_API_URL}/api/production/range`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
                    },
                    body: JSON.stringify(data)
                }),
                fetch(`${PUBLIC_INTERNAL_API_URL}/api/consumption/range`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
                    },
                    body: JSON.stringify(data)
                }),
                fetch(`${PUBLIC_INTERNAL_API_URL}/api/price/range`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
                    },
                    body: JSON.stringify({
                        startTime: data.startTime,
                        endTime: data.endTime
                    })
                })
            ]);

            if (!prodRes.ok || !consRes.ok || !priceRes.ok) {
                console.error(`API error! Production: ${prodRes.status}, Consumption: ${consRes.status}, Price: ${priceRes.status}`);
                return fail(500, { error: "API refusing to serve data..." });
            }

            const productionData = await prodRes.json();
            const consumptionData = await consRes.json();
            const priceData = await priceRes.json();

            const prodFormatted = getFormattedDates(productionData);
            const consFormatted = getFormattedDates(consumptionData);
            const priceFormatted = getFormattedDates(priceData, "startDate", "price");

            // Use the longer label array for the x-axis
            const labels =
                prodFormatted.labels.length >= consFormatted.labels.length
                    ? prodFormatted.labels
                    : consFormatted.labels;

            let productionValues = prodFormatted.values;
            let consumptionValues = consFormatted.values;
            let differenceValues = [];

            const meanProduction = productionValues.reduce((sum, val) => sum + val, 0) / productionValues.length;
            const meanConsumption = consumptionValues.reduce((sum, val) => sum + val, 0) / consumptionValues.length;
            const meanDifference = meanProduction - meanConsumption;

            differenceValues = productionValues.map((val, i) => val - (consumptionValues[i] ?? 0));
            return {
                priceLabels: priceFormatted.labels,
                priceValues: priceFormatted.values,
                labels,
                productionValues,
                consumptionValues,
                differenceValues,
                meanProduction,
                meanConsumption,
                meanDifference,
                startTime: data.startTime,
                endTime: data.endTime,
                selection: data.selection
            };
            
        } catch (e) {
            return fail(500, { error: "Server error" });
        }
    }
};