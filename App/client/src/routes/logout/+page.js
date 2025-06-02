import { error } from "@sveltejs/kit";

export const load = ({ url, params }) => {
  // If there are any params, this is not /logout
  if (Object.keys(params).length > 0) {
    throw error(404, "Page not found.");
  }

  return {
    remove_error: url.searchParams.get("remove_error") === "true",
    removed: url.searchParams.get("removed") === "true",
  };
};