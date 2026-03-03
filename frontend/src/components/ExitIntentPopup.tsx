"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { X, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const COOKIE_NAME = "exit_intent_dismissed";
const SUPPRESS_DAYS = 7;
const MIN_TIME_ON_PAGE_MS = 5000;

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

  useEffect(() => {
    if (getCookie(COOKIE_NAME)) return;
    const timer = setTimeout(() => setReady(true), MIN_TIME_ON_PAGE_MS);
    return () => clearTimeout(timer);
  }, []);

  const dismiss = useCallback(() => {
    setShow(false);
    setCookie(COOKIE_NAME, "1", SUPPRESS_DAYS);
  }, []);

  useEffect(() => {
    if (!ready) return;

    // Desktop: mouse leaves from top
    function onMouseLeave(e: MouseEvent) {
      if (e.clientY <= 50) setShow(true);
    }

    // Mobile: scroll direction change after 25%
    let lastScrollY = window.scrollY;
    let scrollingDown = true;

    function onScroll() {
      const currentY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = docHeight > 0 ? (currentY / docHeight) * 100 : 0;

      if (currentY > lastScrollY) {
        scrollingDown = true;
      } else if (scrollingDown && currentY < lastScrollY && scrollPercent > 25) {
        scrollingDown = false;
        setShow(true);
      }
      lastScrollY = currentY;
    }

    document.addEventListener("mouseleave", onMouseLeave);
    window.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      document.removeEventListener("mouseleave", onMouseLeave);
      window.removeEventListener("scroll", onScroll);
    };
  }, [ready]);

  if (!show) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
      onClick={dismiss}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative mx-4 w-full max-w-md rounded-2xl bg-white p-6 shadow-xl sm:p-8"
      >
        <button
          onClick={dismiss}
          className="absolute right-3 top-3 rounded-full p-2 text-muted-foreground hover:text-foreground"
          aria-label="Închide"
        >
          <X className="size-5" />
        </button>
        <div className="text-center">
          <h2 className="font-display text-xl font-bold text-foreground sm:text-2xl">
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
