import { redirect } from '@sveltejs/kit';
import { useUserState } from "$lib/states/userState.svelte";
import { COOKIE_KEY } from "$env/static/private";

export async function load({ locals, cookies }) {
	cookies.set(COOKIE_KEY, "", {
        httpOnly: true,
        path: '/',
        maxAge: 0
      })
    let userState = useUserState();
    userState.user = null;
    locals.user = null;
    //console.log("logout");

    // redirect to home page
    throw redirect(302, '/');
	
}