import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { decodeJwt } from "jose";
import { COOKIE_KEY } from "$env/static/private";

// handle with decoding only
export const handle = async ({ event, resolve }) => {
  const authCookie = event.cookies.get(COOKIE_KEY);
  if (authCookie) {
    try {
      const payload = decodeJwt(authCookie);
      event.locals.user = payload;
    } catch (e) {
      //console.log(e);
    }
  }

  return await resolve(event);
};

// handle using verify endpoint
const OLDhandle = async ({ event, resolve }) => {
  const authCookie = event.cookies.get(COOKIE_KEY);
  if (authCookie) {
    const response = await fetch(`${PUBLIC_INTERNAL_API_URL}/api/auth/verify`, {
      method: "POST",
      headers: {
        "cookie": `${COOKIE_KEY}=${authCookie}`,
      },
    });

    // if response not ok, clear cookie and resolve
    if (!response.ok) {
      event.cookies.delete(COOKIE_KEY, { path: "/" });
      return await resolve(event);
    }

    const responseCookies = response.headers.getSetCookie();
    const cookie = responseCookies.find((cookie) =>
      cookie.startsWith(COOKIE_KEY)
    );

    // if no cookie, resolve
    if (!cookie) {
      return await resolve(event);
    }

    const cookieValue = cookie.split("=")[1].split(";")[0];
    event.cookies.set(COOKIE_KEY, cookieValue, { path: "/", secure: false });

    try {
      const payload = decodeJwt(authCookie);
      event.locals.user = payload;
    } catch (e) {
      console.log(e);
    }
  }

  return await resolve(event);
};
