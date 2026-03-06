import type { Metadata } from "next";
import { FormWizardClient } from "@/components/form/FormWizardClient";
import { TeamStrip } from "@/components/trust/TeamStrip";
import { TrustBadge } from "@/components/trust/TrustBadge";

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tourism-audit.devidevs.com";

export const metadata: Metadata = {
  title: "Solicită audit digital gratuit",
  description:
    "Completează formularul și primește un raport personalizat cu recomandări practice pentru prezența ta online, în 30-90 de minute.",
  alternates: {
    canonical: "/audit",
  },
  openGraph: {
    title: "Solicită audit digital gratuit | Audit Digital Turism",
    description:
      "Completează formularul și primește un raport personalizat cu recomandări practice pentru prezența ta online, în 30-90 de minute.",
    type: "website",
    url: `${siteUrl}/audit`,
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Audit Digital Turism",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Solicită audit digital gratuit | Audit Digital Turism",
    description: "Raport personalizat cu recomandări practice pentru prezența ta online, în 30-90 de minute.",
    images: ["/preview-image.png"],
  },
};

// ISR: revalidate every 7 days
export const revalidate = 604800;

const breadcrumbJsonLd = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    {
      "@type": "ListItem",
      position: 1,
      name: "Acasă",
      item: `${siteUrl}/marketing-pentru-turism`,
    },
    {
      "@type": "ListItem",
      position: 2,
      name: "Audit digital gratuit",
      item: `${siteUrl}/audit`,
    },
  ],
};

export default function AuditPage() {
  const meetingLink = process.env.MEETING_LINK;

  return (
    <div className="bg-gradient-hero">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
      />
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
