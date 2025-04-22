import { browser } from "$app/environment";
import * as dataApi from "$lib/apis/data-api.js";

let pricesState = $state({});

if (browser) {
  pricesState = await dataApi.readPublicData();
}

const usePricesState = () => {
  return {
    get data() {
      return pricesState;
    },
    update: async () => {
      pricesState = await dataApi.readPublicData();
    },
    // this is a trick for chart.js to get the data
    // it needs to be a plain object
    // otherwise it will not work
    state2js: () => {
      return JSON.parse(JSON.stringify(pricesState));
    },
  }
};

export { usePricesState };