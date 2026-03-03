"use client";

import { usePathname, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { pageview } from "@/lib/gtag";
import { captureUTMParams } from "@/lib/utm";

export function GAListener() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    captureUTMParams();
  }, [searchParams]);

  useEffect(() => {
    pageview(pathname);
  }, [pathname]);

  return null;
}
