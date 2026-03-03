import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enabled: !!process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
  ignoreErrors: [
    "chrome-extension://",
    "moz-extension://",
    "NetworkError",
    "Failed to fetch",
    "Load failed",
    "AbortError",
  ],
  beforeSend(event) {
    if (event.request) {
      delete event.request.cookies;
    }
    return event;
  },
});
