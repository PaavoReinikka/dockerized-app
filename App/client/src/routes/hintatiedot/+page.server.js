// src/routes/protected/+page.server.js
import { redirect } from '@sveltejs/kit';
import { COOKIE_KEY } from "$env/static/private";


// NOTE: Markus, älä mielellään kajoa noihin session-käytäntöihin, koska ne hoidetaan jo muualla,
// ja vaarana on että session hallinta menee sekaisin, jos niitä muokataan ohimennen.
// Älä myöskään koske kekseihin, jos et ole ihan 100 varmana mitä teet.
// Jos haluat esim. tarkistaa onko käyttäjä kirjautunut sisään, hyödynnä JWT tokenin payloadia,
// joka on jo valmiiksi saatavilla (laitan sen hookseissa).

// This function checks if the user is authenticated by looking for a session cookie.
// export async function load({ cookies }) {
// 	const session = cookies.get(COOKIE_KEY);

// 	if (!session) {
// 		throw redirect(302, '/auth/login');
// 	}

// 	// Optionally pass user session data to the page:
// 	return {
// 		user: { session }
// 	};
// }
