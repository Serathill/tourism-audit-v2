"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import Link from "next/link";
import { X, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const COOKIE_NAME = "exit_intent_dismissed";
const SUPPRESS_DAYS = 7;
const MIN_TIME_ON_PAGE_MS = 5000;
const MOBILE_IDLE_MS = 45000; // 45s inactivity on mobile before showing

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? match[2] : null;
}

function setCookie(name: string, value: string, days: number): void {
  const expires = new Date(Date.now() + days * 86400000).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}

export function ExitIntentPopup() {
  const [show, setShow] = useState(false);
  const [ready, setReady] = useState(false);
  const [triggered, setTriggered] = useState(false);
  const closeRef = useRef<HTMLButtonElement>(null);
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (getCookie(COOKIE_NAME)) return;
    const timer = setTimeout(() => setReady(true), MIN_TIME_ON_PAGE_MS);
    return () => clearTimeout(timer);
  }, []);

  const dismiss = useCallback(() => {
    setShow(false);
    setTriggered(true);
    setCookie(COOKIE_NAME, "1", SUPPRESS_DAYS);
  }, []);

  useEffect(() => {
    if (!ready || triggered) return;

    const isTouch = window.matchMedia("(pointer: coarse)").matches;

    function trigger() {
      setShow(true);
      setTriggered(true);
    }

    if (!isTouch) {
      // Desktop: mouse leaves from top — standard exit intent
      function onMouseLeave(e: MouseEvent) {
        if (e.clientY <= 50) trigger();
      }
      document.addEventListener("mouseleave", onMouseLeave);
      return () => document.removeEventListener("mouseleave", onMouseLeave);
    }

    // Mobile: idle timer — show after 45s of no interaction
    let idleTimer = setTimeout(trigger, MOBILE_IDLE_MS);

    function resetIdle() {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(trigger, MOBILE_IDLE_MS);
    }

    window.addEventListener("scroll", resetIdle, { passive: true });
    window.addEventListener("touchstart", resetIdle, { passive: true });

    return () => {
      clearTimeout(idleTimer);
      window.removeEventListener("scroll", resetIdle);
      window.removeEventListener("touchstart", resetIdle);
    };
  }, [ready, triggered]);

  // Focus trap + keyboard handling
  useEffect(() => {
    if (!show) return;

    // Focus close button on open
    closeRef.current?.focus();

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        dismiss();
        return;
      }
      if (e.key !== "Tab" || !dialogRef.current) return;

      const focusable = dialogRef.current.querySelectorAll<HTMLElement>(
        'button, [href], input, [tabindex]:not([tabindex="-1"])'
      );
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last?.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first?.focus();
      }
    }

    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [show, dismiss]);

  if (!show) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
      onClick={dismiss}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="exit-intent-heading"
        onClick={(e) => e.stopPropagation()}
        className="relative mx-4 w-full max-w-md rounded-2xl bg-white p-6 shadow-xl sm:p-8"
      >
        <button
          ref={closeRef}
          onClick={dismiss}
          className="absolute right-3 top-3 rounded-full p-2 text-muted-foreground hover:text-foreground"
          aria-label="Închide"
        >
          <X className="size-5" />
        </button>
        <div className="text-center">
          <h2 id="exit-intent-heading" className="font-display text-xl font-bold text-foreground sm:text-2xl">
            Nu pleca fără auditul tău gratuit!
          </h2>
          <p className="mt-3 text-sm text-muted-foreground">
            Află în doar 30 de minute ce poți îmbunătăți la prezența ta online.
            Este complet gratuit.
          </p>
          <Button
            asChild
            className="mt-6 w-full bg-gradient-cta font-semibold text-foreground shadow-md"
          >
            <Link href="/audit" onClick={dismiss}>
              Solicită auditul gratuit
              <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
