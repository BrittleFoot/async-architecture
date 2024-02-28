import type { Session } from "@auth/sveltekit";
import { UserService } from "./api/user";
import { getTokenInfo } from "./auth";


export async function getMe(session: Session | null): Promise<User | null> {
    let { tokenInfo } = await getTokenInfo(session);
    if (!tokenInfo) {
        return null;
    }
    let userService = new UserService(tokenInfo.accessToken);
    return await userService.getMe();
}