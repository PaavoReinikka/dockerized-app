import { error, redirect } from "@sveltejs/kit";

export const load = async ({ locals, url }) => {
  if (!locals.user) {
    // Not logged in, redirect to login
    throw redirect(303, `/auth/login`);
  }
  // Optionally, check for roles/privileges:
  if (locals.user.role !== "admin" ) throw error(403, "Forbidden");
  return {};
};