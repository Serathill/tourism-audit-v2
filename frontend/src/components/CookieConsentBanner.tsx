"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

const COOKIE_NAME = "cookie_consent";
const COOKIE_DAYS = 365;

type ConsentState = {
  analytics_storage: "granted" | "denied";
  ad_storage: "granted" | "denied";
  ad_user_data: "granted" | "denied";
  ad_personalization: "granted" | "denied";
};

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? match[2] : null;
}

function setCookie(name: string, value: string, days: number): void {
  const expires = new Date(Date.now() + days * 86400000).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}

function updateConsent(consent: ConsentState) {
  if (typeof window !== "undefined" && window.gtag) {
    window.gtag("consent", "update", consent);
  }
}

export function CookieConsentBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const existing = getCookie(COOKIE_NAME);
    if (!existing) {
      setVisible(true);
    } else {
      try {
        const consent = JSON.parse(existing) as ConsentState;
        updateConsent(consent);
      } catch {
        setVisible(true);
      }
    }
  }, []);

  function accept() {
    const consent: ConsentState = {
      analytics_storage: "granted",
      ad_storage: "granted",
      ad_user_data: "granted",
      ad_personalization: "granted",
    };
    setCookie(COOKIE_NAME, JSON.stringify(consent), COOKIE_DAYS);
    updateConsent(consent);
    setVisible(false);
  }

  function reject() {
    const consent: ConsentState = {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    };
    setCookie(COOKIE_NAME, JSON.stringify(consent), COOKIE_DAYS);
    updateConsent(consent);
    setVisible(false);
  }

  function acceptAnalyticsOnly() {
    const consent: ConsentState = {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    };
    setCookie(COOKIE_NAME, JSON.stringify(consent), COOKIE_DAYS);
    updateConsent(consent);
    setVisible(false);
  }

  if (!visible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-white p-4 pb-[max(1rem,env(safe-area-inset-bottom))] shadow-lg sm:p-6 sm:pb-[max(1.5rem,env(safe-area-inset-bottom))]">
      <div className="mx-auto flex max-w-4xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex-1">
          <p className="text-sm text-foreground font-medium">
            Folosim cookies pentru a îmbunătăți experiența ta
          </p>
          <p className="mt-1 text-xs text-muted-foreground">
            Poți alege ce tipuri de cookies permiți. Vezi{" "}
            <a href="/privacy-policy" className="text-primary hover:underline">
              politica de confidențialitate
            </a>
            .
          </p>
        </div>
        <div className="flex w-full flex-col gap-2 sm:w-auto sm:flex-row">
          <Button onClick={reject} variant="outline" size="default" className="w-full sm:w-auto">
            Refuză
          </Button>
          <Button onClick={acceptAnalyticsOnly} variant="secondary" size="default" className="w-full sm:w-auto">
            Doar analitice
          </Button>
          <Button onClick={accept} size="default" className="w-full sm:w-auto">
            Accept toate
          </Button>
        </div>
      </div>
    </div>
  );
}

export function ManageCookiesButton() {
  function resetConsent() {
    document.cookie = `${COOKIE_NAME}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    window.location.reload();
  }

  return (
    <button
      onClick={resetConsent}
      className="text-left text-sm text-slate-300 transition-colors hover:text-white"
    >
      Gestionează cookie-uri
    </button>
  );
}
