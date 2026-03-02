import type { Metadata } from "next";
import { FormWizardClient } from "@/components/form/FormWizardClient";
import { TeamStrip } from "@/components/trust/TeamStrip";
import { TrustBadge } from "@/components/trust/TrustBadge";

export const metadata: Metadata = {
  title: "Solicită audit digital gratuit",
  description:
    "Completează formularul și primește un raport personalizat cu recomandări practice pentru prezența ta online, în 30-90 de minute.",
  alternates: {
    canonical: "/audit",
  },
};

export default function AuditPage() {
  const meetingLink = process.env.MEETING_LINK;

  return (
    <div className="bg-gradient-hero">
      <div className="mx-auto max-w-xl px-4 py-12 sm:px-6 md:py-16">
        <div className="mb-8 text-center">
          <h1 className="font-display text-[clamp(1.5rem,4vw,2.25rem)] font-bold tracking-tight text-foreground">
            Solicită audit digital gratuit
          </h1>
          <p className="mt-3 text-muted-foreground">
            Completează formularul și primești un raport personalizat în 30-90
            de minute
          </p>
          <div className="mt-4 flex justify-center">
            <TeamStrip />
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-white p-6 shadow-md sm:p-8">
          <FormWizardClient meetingLink={meetingLink} />
        </div>

        <div className="mt-4 flex justify-center">
          <TrustBadge />
        </div>
      </div>
    </div>
  );
}
