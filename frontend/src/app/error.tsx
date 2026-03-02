"use client";

import { useEffect } from "react";
import * as Sentry from "@sentry/nextjs";
import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function RootError({
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
    <div className="flex min-h-[60vh] items-center justify-center px-4">
      <div className="mx-auto flex max-w-md flex-col items-center gap-4 text-center">
        <div className="flex size-12 items-center justify-center rounded-full bg-destructive/10">
          <AlertTriangle className="size-6 text-destructive" />
        </div>
        <h2 className="font-display text-xl font-bold text-foreground">
          A apărut o eroare neașteptată
        </h2>
        <p className="text-sm text-muted-foreground">
          Te rugăm încearcă din nou. Dacă problema persistă, contactează-ne.
        </p>
        <Button onClick={reset} variant="outline">
          Încearcă din nou
        </Button>
      </div>
    </div>
  );
}
