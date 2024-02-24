import { redirect } from "@sveltejs/kit"
import { signOut } from "../../auth"
import type { Actions } from "./$types"

export const actions: Actions = {
    default:
        async (event) => {
            let session = await event.locals.auth();

            if (!session?.user) {
                throw redirect(302, '/');
            }

            await signOut(event);
        }
}


export const load = async (event) => {
    let session = await event.locals.auth();

    if (!session?.user) {
        throw redirect(302, '/');
    }
}