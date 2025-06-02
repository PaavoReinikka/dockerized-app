import { json } from '@sveltejs/kit';
import { PUBLIC_INTERNAL_CHAT_URL } from '$env/static/public';

/*
The purpose of this endpoint is to check if the chat service is available.
*/
export const GET= async () => {
    try {
        const res = await fetch(`${PUBLIC_INTERNAL_CHAT_URL}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const text = await res.text();
        // Check if response is HTML
        if (res.ok && text.trim().startsWith('<!doctype html>')) {
            console.log('Chat service is available');
            return json({ available: true });
        }
    } catch (e) {}
    return json({ available: false });
}