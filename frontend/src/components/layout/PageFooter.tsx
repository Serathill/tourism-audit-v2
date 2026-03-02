import Link from "next/link";
import { ExternalLink } from "lucide-react";
import { BRAND, NAV_LINKS, AUDIT_CTA_LINK, LEGAL_LINKS } from "@/lib/constants";

export function PageFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer role="contentinfo" className="bg-[#0F172A] text-slate-300">
      <div className="mx-auto max-w-[1200px] px-4 py-12 sm:px-6">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {/* Brand column */}
          <div className="flex flex-col gap-3">
            <span className="font-display text-lg font-bold text-white">
              {BRAND.name}
            </span>
            <p className="text-sm leading-relaxed text-slate-400">
              {BRAND.tagline}
            </p>
            <a
              href={BRAND.parentUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-medium text-brand-teal-lighter transition-colors hover:text-brand-teal-light"
            >
              Vizitează {BRAND.parentName}
              <ExternalLink className="size-3.5" />
            </a>
          </div>

          {/* Pages column */}
          <div className="flex flex-col gap-3">
            <span className="text-sm font-semibold uppercase tracking-wider text-slate-500">
              Pagini
            </span>
            <nav aria-label="Navigare footer — pagini" className="flex flex-col gap-2">
              {[...NAV_LINKS, AUDIT_CTA_LINK].map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-sm text-slate-400 transition-colors hover:text-white"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>

          {/* Legal column */}
          <div className="flex flex-col gap-3">
            <span className="text-sm font-semibold uppercase tracking-wider text-slate-500">
              Legal
            </span>
            <nav aria-label="Navigare footer — legal" className="flex flex-col gap-2">
              {LEGAL_LINKS.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-sm text-slate-400 transition-colors hover:text-white"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 border-t border-slate-800 pt-6 text-center text-xs text-slate-500">
          &copy; {currentYear} {BRAND.parentName}. Toate drepturile rezervate.
        </div>
      </div>
    </footer>
  );
}
