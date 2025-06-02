import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { datesInOrder, getFormattedDates } from '$lib/utils/date-helpers.js';
import { fail } from "@sveltejs/kit";
import { COOKIE_KEY } from "$env/static/private";


export const actions = {
  getPriceRangeAll: async ({ request, cookies }) => {
    const fdata = await request.formData();
    const data = Object.fromEntries(fdata);

    if (!data.startTime || !data.endTime) {
      return fail(400, { error: "Start and end dates are required." });
    } else if (!datesInOrder(data.startTime, data.endTime)) {
      return fail(400, { error: "Start date must be before end date." });
    }

    try {
      // Fetch all three datasets in parallel
      const [plainRes, weekdayRes, hourlyRes] = await Promise.all([
        fetch(`${PUBLIC_INTERNAL_API_URL}/api/price/range`, {
          method: "POST",
          headers: { "Content-Type": "application/json", cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}` },
          body: JSON.stringify(data)
        }),
        fetch(`${PUBLIC_INTERNAL_API_URL}/api/price/weekdayavg`, {
          method: "POST",
          headers: { "Content-Type": "application/json", cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}` },
          body: JSON.stringify(data)
        }),
        fetch(`${PUBLIC_INTERNAL_API_URL}/api/price/hourlyavg`, {
          method: "POST",
          headers: { "Content-Type": "application/json", cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}` },
          body: JSON.stringify(data)
        })
      ]);

      if (!plainRes.ok || !weekdayRes.ok || !hourlyRes.ok) {
        return fail(500, { error: "API refusing to serve data..." });
      }

      // Parse all datasets
      const plainData = await plainRes.json();
      const weekdayData = await weekdayRes.json();
      const hourlyData = await hourlyRes.json();

      const plainSorted = getFormattedDates(plainData, "startDate", "price");
      const plainLabels = plainSorted.labels;
      const plainValues = plainSorted.values;

      // Format weekday avg (sort by weekday 0-6, label as weekday name)
      const weekdayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
      const weekdaySorted = [...weekdayData].sort((a, b) => a.weekday - b.weekday);
      const weekdayLabels = weekdaySorted.map(item => weekdayNames[item.weekday % 7]);
      const weekdayValues = weekdaySorted.map(item => item.avgPrice);
      // flip sunday to be the last day
      weekdayLabels.push(weekdayLabels.shift());
      weekdayValues.push(weekdayValues.shift());

      // Format hourly avg (sort by hour 0-23, label as "00:00", "01:00", ...)
      const hourlySorted = [...hourlyData].sort((a, b) => a.hour - b.hour);
      const hourlyLabels = hourlySorted.map(item => `${item.hour.toString().padStart(2, "0")}:00`);
      const hourlyValues = hourlySorted.map(item => item.avgPrice);

      return {
        plainPriceLabels: plainLabels,
        plainPriceValues: plainValues,
        weekdayPriceLabels: weekdayLabels,
        weekdayPriceValues: weekdayValues,
        hourlyPriceLabels: hourlyLabels,
        hourlyPriceValues: hourlyValues,
        startTime: data.startTime,
        endTime: data.endTime
      };
    } catch (e) {
      return fail(500, { error: "Server error" });
    }
  }
};

const OLDactions = {
  getProductionRange: async ({ request, cookies }) => {
    const fdata = await request.formData();
    const data = Object.fromEntries(fdata);

    if (!data.startTime || !data.endTime) {
      return fail(400, { error: "Start and end dates are required." });
    } else if (!datesInOrder(data.startTime, data.endTime)) {
      return fail(400, { error: "Start date must be before end date." });
    }

    try {
      const res = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/production/range`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
            cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
         },
        body: JSON.stringify(data)
      });

      if (!res.ok) {
        return fail(res.status, { error: "API refusing to serve data..." });
      }

      const productionData = await res.json();
      const { values, labels } = getFormattedDates(productionData);
      return { 
        productionValues: values,
        productionLabels: labels,
        startTime: data.startTime,
        endTime: data.endTime
      };
    } catch (e) {
      return fail(500, { error: "Server error" });
    }
  },

  getConsumptionRange: async ({ request, cookies }) => {
    const fdata = await request.formData();
    const data = Object.fromEntries(fdata);

    if (!data.startTime || !data.endTime) {
      return fail(400, { error: "Start and end dates are required." });
    } else if (!datesInOrder(data.startTime, data.endTime)) {
      return fail(400, { error: "Start date must be before end date." });
    }

    try {
      const res = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/consumption/range`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
            cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
         },
        body: JSON.stringify(data)
      });

      if (!res.ok) {
        return fail(res.status, { error: "API refusing to serve data..." });
      }

      const consumptionData = await res.json();
      const { values, labels } = getFormattedDates(consumptionData);
      return { 
        consumptionValues: values,
        consumptionLabels: labels,
        startTime: data.startTime,
        endTime: data.endTime
      };
    } catch (e) {
      return fail(500, { error: "Server error" });
    }
  },
  getPriceRange: async ({ request, cookies }) => {
    const fdata = await request.formData();
    const data = Object.fromEntries(fdata);

    if (!data.startTime || !data.endTime) {
      return fail(400, { error: "Start and end dates are required." });
    } else if (!datesInOrder(data.startTime, data.endTime)) {
      return fail(400, { error: "Start date must be before end date." });
    }

    try {
      const res = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/price/range`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
            cookie: `${COOKIE_KEY}=${cookies.get(COOKIE_KEY)}`
         },
        body: JSON.stringify({
          startTime: data.startTime,
          endTime: data.endTime
        })
      });

      if (!res.ok) {
        return fail(res.status, { error: "API refusing to serve data..." });
      }

      const priceData = await res.json();
      const datetimesUTC = priceData.map(item => item.startDate);
      const datetimesHelsinki = datetimesUTC.map(dt =>
        new Date(dt).toLocaleString("fi-FI", {
          timeZone: "Europe/Helsinki",
          year: "numeric",
          month: "numeric",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit"
        })
      );
      const priceValues = priceData.map(item => item.price);

      return { 
        priceValues,
        priceLabels: datetimesHelsinki,
        startTime: data.startTime,
        endTime: data.endTime
      };
    } catch (e) {
      return fail(500, { error: "Server error" });
    }
  }
  
};