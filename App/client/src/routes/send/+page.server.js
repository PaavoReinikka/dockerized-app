import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { redirect } from "@sveltejs/kit";
import { COOKIE_KEY } from "$env/static/private";

const apiRequest = async (url, data) => {
  return await fetch(`${PUBLIC_INTERNAL_API_URL}${url}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
};

export const actions = {

  resend: async ({ request, cookies }) => {
    const data = await request.formData();
    const response = await apiRequest(
      "/api/auth/resend",
      Object.fromEntries(data),
    );
    return response.json();
  }
};