// $lib/states/usePricesState.js
import { browser } from "$app/environment";
import * as dataApi from "$lib/apis/data-api.js";

let pricesState = $state([]); // Use empty array as default

if (browser) {
  pricesState = await dataApi.readPublicData()
}

const usePricesState = () => {
  return {
    get data() {
      return pricesState;
    },
    update: async () => {
      pricesState = await dataApi.readPublicData();
    },
    state2js: () => {
      return JSON.parse(JSON.stringify(pricesState));
    },
    get values() {
      return pricesState.map((item) => item.value);
    },
    get labels() {
      return pricesState.map((item) => item.startDate);
    },
  };
};

export { usePricesState };
