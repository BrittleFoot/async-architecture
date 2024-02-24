import { redirect } from "@sveltejs/kit";
import { signIn } from "../../auth"
import type { Actions } from "./$types"

export const actions: Actions = {
    default:
        async (event) => {
            let session = await event.locals.auth();

            if (session?.user) {
                throw redirect(302, '/');
            }

            await signIn(event);
        }
}

export const load = async (event) => {
    let session = await event.locals.auth();

    if (session?.user) {
        throw redirect(302, '/');
    }
}