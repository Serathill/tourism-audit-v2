import type { Metadata } from "next";
import { HeroSection } from "@/components/sections/HeroSection";
import { AudienceSection } from "@/components/sections/AudienceSection";
import { ProcessSection } from "@/components/sections/ProcessSection";
import { WhyUsSection } from "@/components/sections/WhyUsSection";
import { FinalCtaSection } from "@/components/sections/FinalCtaSection";
import { SectionDivider } from "@/components/layout/SectionDivider";

export const metadata: Metadata = {
  title: "Marketing pentru turism & audit digital gratuit | DeviDevs Agency",
  description:
    "Primește un audit digital gratuit pentru pensiunea sau unitatea ta de cazare. Analizăm prezența online folosind doar informații publice. Rezultate în 30-90 minute.",
  alternates: {
    canonical: "/marketing-pentru-turism",
  },
  openGraph: {
    title: "Marketing pentru turism & audit digital gratuit | DeviDevs Agency",
    type: "website",
    url: "https://audit.devidevs.com/marketing-pentru-turism",
    images: [
      {
        url: "/preview-image.png",
        width: 1200,
        height: 630,
        alt: "Audit Digital Turism",
      },
    ],
  },
  twitter: { card: "summary_large_image", images: ["/preview-image.png"] },
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
      item: "https://audit.devidevs.com/marketing-pentru-turism",
    },
  ],
};

export default function MarketingPentruTurismPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
      />
      <HeroSection />
      <SectionDivider />
      <AudienceSection />
      <SectionDivider />
      <ProcessSection />
      <SectionDivider />
      <WhyUsSection />
      <SectionDivider />
      <FinalCtaSection />
    </>
  );
}
