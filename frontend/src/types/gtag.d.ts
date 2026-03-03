declare global {
  interface Window {
    gtag: (
      command: "config" | "event" | "consent" | "js" | "set",
      targetOrName: string | Date,
      params?: Record<string, unknown>
    ) => void;
    dataLayer: Array<unknown>;
  }
}

export {};
