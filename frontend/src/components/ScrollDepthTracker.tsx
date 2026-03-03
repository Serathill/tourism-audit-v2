"use client";

import { useEffect, useRef } from "react";
import { trackScrollDepth } from "@/lib/gtag";

const THRESHOLDS = [25, 50, 75, 100] as const;

export function ScrollDepthTracker() {
  const firedRef = useRef(new Set<number>());

  useEffect(() => {
    let ticking = false;

    function onScroll() {
      if (ticking) return;
      ticking = true;

      requestAnimationFrame(() => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight <= 0) { ticking = false; return; }

        const percent = Math.round((scrollTop / docHeight) * 100);

        for (const threshold of THRESHOLDS) {
          if (percent >= threshold && !firedRef.current.has(threshold)) {
            firedRef.current.add(threshold);
            trackScrollDepth(threshold);
          }
        }
        ticking = false;
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return null;
}
