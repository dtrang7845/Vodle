export type FontSizePreference = "small" | "medium" | "large"

export const FONT_SIZE_KEY = "vodle_font_size"
export const NOTIFICATIONS_KEY = "vodle_daily_notifications"

export function getStoredFontSize(): FontSizePreference {
  if (typeof window === "undefined") {
    return "medium"
  }

  const storedValue = window.localStorage.getItem(FONT_SIZE_KEY)
  if (
    storedValue === "small" ||
    storedValue === "medium" ||
    storedValue === "large"
  ) {
    return storedValue
  }

  return "medium"
}

export function applyFontSize(fontSize: FontSizePreference) {
  if (typeof document === "undefined") {
    return
  }

  document.documentElement.dataset.fontSize = fontSize
}

export function setStoredFontSize(fontSize: FontSizePreference) {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(FONT_SIZE_KEY, fontSize)
  }
  applyFontSize(fontSize)
}

export function getStoredNotificationsPreference() {
  if (typeof window === "undefined") {
    return false
  }

  return window.localStorage.getItem(NOTIFICATIONS_KEY) === "true"
}

export function setStoredNotificationsPreference(enabled: boolean) {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(NOTIFICATIONS_KEY, String(enabled))
  }
}
