const ACCESS_TOKEN_KEY = "vodle_access_token";

export function getAccessToken() {
  if (typeof window === "undefined") {
    return null;
  }

  return window.localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function saveAccessToken(token: string) {
  window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function clearAccessToken() {
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  }
}

export function authHeaders(headers?: HeadersInit): HeadersInit {
  const token = getAccessToken();
  if (!token) {
    return headers ?? {};
  }

  return {
    ...headers,
    Authorization: `Bearer ${token}`,
  };
}

export function authFetch(input: RequestInfo | URL, init?: RequestInit) {
  return fetch(input, {
    ...init,
    credentials: "include",
    headers: authHeaders(init?.headers),
  });
}

export async function logoutUser(apiBaseUrl: string) {
  await fetch(`${apiBaseUrl}/api/v1/user/logout`, {
    method: "POST",
    credentials: "include",
  }).catch(() => undefined);
  clearAccessToken();
}
