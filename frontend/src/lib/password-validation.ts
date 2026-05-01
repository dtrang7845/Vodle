export const PASSWORD_REQUIREMENTS = [
  "At least 8 characters",
  "At least 1 uppercase letter",
  "At least 1 special character",
] as const

export function getPasswordValidationError(password: string) {
  if (password.length < 8) {
    return "Password must be at least 8 characters long."
  }

  if (!/[A-Z]/.test(password)) {
    return "Password must include at least one uppercase letter."
  }

  if (!/[^A-Za-z0-9]/.test(password)) {
    return "Password must include at least one special character."
  }

  return null
}
