// $lib/states/usePricesState.js
import { browser } from "$app/environment";
import * as dataApi from "$lib/apis/data-api.js";

let pricesState = $state([]); // Use empty array as default

const usePricesState = () => {
  return {
    get data() {
      return pricesState;
    },
    load: async () => {
      if (browser) {
        try {
          const result = await dataApi.readPublicData();
          pricesState = result;
        } catch (e) {
          console.error("Failed to load pricesState:", e);
          pricesState = [];
        }
      }
    },
    state2js: () => {
      return JSON.parse(JSON.stringify(pricesState));
    },
  };
};

export { usePricesState };
