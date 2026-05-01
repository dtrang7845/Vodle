export async function logoutUser(apiBaseUrl: string) {
  await fetch(`${apiBaseUrl}/api/v1/user/logout`, {
    method: "POST",
    credentials: "include",
  }).catch(() => undefined);
}
