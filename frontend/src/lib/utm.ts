const UTM_STORAGE_KEY = "utm_params";

const UTM_KEYS = [
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
] as const;

type UTMParams = Partial<Record<(typeof UTM_KEYS)[number], string>>;

export function captureUTMParams(): void {
  if (typeof window === "undefined") return;

  const searchParams = new URLSearchParams(window.location.search);
  const params: UTMParams = {};
  let hasUTM = false;

  for (const key of UTM_KEYS) {
    const value = searchParams.get(key);
    if (value) {
      params[key] = value;
      hasUTM = true;
    }
  }

  if (hasUTM) {
    try {
      localStorage.setItem(UTM_STORAGE_KEY, JSON.stringify(params));
    } catch {
      // localStorage unavailable
    }
  }
}

export function getStoredUTMParams(): UTMParams {
  if (typeof window === "undefined") return {};

  try {
    const stored = localStorage.getItem(UTM_STORAGE_KEY);
    if (stored) return JSON.parse(stored) as UTMParams;
  } catch {
    // localStorage unavailable or corrupted
  }
  return {};
}
