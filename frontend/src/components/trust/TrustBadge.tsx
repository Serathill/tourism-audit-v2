import { Shield } from "lucide-react";

export function TrustBadge() {
  return (
    <div className="inline-flex items-center gap-2 rounded-full border border-brand-teal-lighter bg-brand-teal-lightest px-4 py-2">
      <Shield className="size-4 shrink-0 text-primary" />
      <span className="text-sm font-medium text-brand-teal-dark">
        Fără acces la date interne — analiză din surse publice
      </span>
    </div>
  );
}
