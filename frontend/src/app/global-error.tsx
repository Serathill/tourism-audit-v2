"use client";

import * as Sentry from "@sentry/nextjs";
import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <html lang="ro">
      <body>
        <div style={{ display: "flex", minHeight: "100vh", alignItems: "center", justifyContent: "center", padding: "1rem" }}>
          <div style={{ textAlign: "center", maxWidth: "28rem" }}>
            <h2 style={{ fontSize: "1.25rem", fontWeight: 700 }}>
              A apărut o eroare neașteptată
            </h2>
            <p style={{ marginTop: "0.5rem", color: "#6b7280" }}>
              Te rugăm încearcă din nou.
            </p>
            <button
              onClick={reset}
              style={{
                marginTop: "1rem",
                padding: "0.5rem 1.5rem",
                borderRadius: "0.5rem",
                border: "1px solid #d1d5db",
                cursor: "pointer",
              }}
            >
              Încearcă din nou
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
