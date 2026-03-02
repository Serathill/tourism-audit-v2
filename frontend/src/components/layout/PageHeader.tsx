"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { NAV_LINKS, AUDIT_CTA_LINK, BRAND } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function PageHeader() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-transparent bg-white/90 backdrop-blur-xl backdrop-saturate-[180%] transition-[border-color,box-shadow] duration-300 [&:has(+main:not(:first-child))]:border-border [&:has(+main:not(:first-child))]:shadow-sm">
      <nav
        aria-label="Navigare principală"
        className="mx-auto flex h-16 max-w-[1200px] items-center justify-between px-4 sm:px-6"
      >
        {/* Logo */}
        <Link
          href="/marketing-pentru-turism"
          className="font-display text-lg font-bold tracking-tight text-foreground transition-colors hover:text-primary"
        >
          {BRAND.name}
        </Link>

        {/* Desktop nav */}
        <div className="hidden items-center gap-1 md:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-muted hover:text-foreground",
                pathname === link.href
                  ? "text-primary"
                  : "text-muted-foreground"
              )}
            >
              {link.label}
            </Link>
          ))}
          <Button asChild size="sm" className="ml-2 bg-gradient-cta text-foreground font-semibold shadow-sm hover:shadow-md transition-shadow">
            <Link href={AUDIT_CTA_LINK.href}>{AUDIT_CTA_LINK.label}</Link>
          </Button>
        </div>

        {/* Mobile hamburger */}
        <button
          type="button"
          onClick={() => setMobileOpen(!mobileOpen)}
          className="inline-flex items-center justify-center rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground md:hidden"
          aria-label={mobileOpen ? "Închide meniul" : "Deschide meniul"}
          aria-expanded={mobileOpen}
        >
          {mobileOpen ? (
            <X className="size-5" />
          ) : (
            <Menu className="size-5" />
          )}
        </button>
      </nav>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="border-t border-border bg-white px-4 pb-4 pt-2 md:hidden">
          <div className="flex flex-col gap-1">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className={cn(
                  "rounded-lg px-3 py-3 text-sm font-medium transition-colors hover:bg-muted",
                  pathname === link.href
                    ? "text-primary bg-primary/5"
                    : "text-foreground"
                )}
              >
                {link.label}
              </Link>
            ))}
            <Button
              asChild
              className="mt-2 w-full bg-gradient-cta text-foreground font-semibold"
            >
              <Link
                href={AUDIT_CTA_LINK.href}
                onClick={() => setMobileOpen(false)}
              >
                {AUDIT_CTA_LINK.label}
              </Link>
            </Button>
          </div>
        </div>
      )}
    </header>
  );
}
