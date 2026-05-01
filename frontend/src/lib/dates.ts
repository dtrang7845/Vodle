export function parseDateOnly(date: string) {
  const [year, month, day] = date.split("-").map(Number);
  return new Date(year, month - 1, day);
}

export function formatDateOnly(
  date: string,
  options: Intl.DateTimeFormatOptions,
) {
  return parseDateOnly(date).toLocaleDateString("en-US", options);
}
