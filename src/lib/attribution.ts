const STORAGE_KEY = "deo-core-attribution";
const UTM_KEYS = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
] as const;
type Attribution = Partial<
  Record<(typeof UTM_KEYS)[number] | "referrer", string>
>;
/** Store campaign metadata only; never contacts, descriptions or file contents. */
export function captureAttribution(): Attribution {
  const current: Attribution = {};
  const url = new URL(window.location.href);
  for (const key of UTM_KEYS) {
    const value = url.searchParams.get(key);
    if (value) current[key] = value.slice(0, 250);
  }
  let saved: Attribution = {};
  try {
    const parsed: unknown = JSON.parse(
      sessionStorage.getItem(STORAGE_KEY) || "{}",
    );
    if (parsed && typeof parsed === "object")
      for (const key of [...UTM_KEYS, "referrer"] as const) {
        const value = (parsed as Record<string, unknown>)[key];
        if (typeof value === "string")
          saved[key] = value.slice(0, key === "referrer" ? 2000 : 250);
      }
  } catch {
    /* Storage can be disabled by the browser. */
  }
  saved = {
    ...saved,
    ...current,
    referrer: saved.referrer ?? document.referrer.slice(0, 2000),
  };
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
  } catch {
    /* No storage is required to submit a request. */
  }
  return saved;
}
