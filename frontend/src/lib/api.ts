function resolveApiBaseUrl() {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }

  if (typeof window !== "undefined") {
    const host =
      window.location.hostname === "127.0.0.1" ? "127.0.0.1" : "localhost";
    return `http://${host}:8000`;
  }

  return "http://localhost:8000";
}

export const API_BASE_URL = resolveApiBaseUrl();
