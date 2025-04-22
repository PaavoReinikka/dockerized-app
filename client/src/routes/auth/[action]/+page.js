import { error } from "@sveltejs/kit";

export const load = ({ params, url }) => {
  if (params.action !== "login" && params.action !== "register") {
    throw error(404, "Page not found.");
  }

  if (url.searchParams.has("registered")) {
    params.registered = true;
  }

  return params;
};