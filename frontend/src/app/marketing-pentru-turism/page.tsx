import type { Metadata } from "next";
import { HeroSection } from "@/components/sections/HeroSection";
import { AudienceSection } from "@/components/sections/AudienceSection";
import { ProcessSection } from "@/components/sections/ProcessSection";
import { WhyUsSection } from "@/components/sections/WhyUsSection";
import { FaqSection } from "@/components/sections/FaqSection";
import { FinalCtaSection } from "@/components/sections/FinalCtaSection";
import { SectionDivider } from "@/components/layout/SectionDivider";

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL || "https://tourism-audit.devidevs.com";

export const metadata: Metadata = {
  title:
    "Marketing pentru turism — audit digital gratuit | DeviDevs Agency",
  description:
    "Audit digital gratuit pentru pensiuni, case de vacanță și unități de cazare din România. Află unde pierzi vizibilitate online. Raport personalizat în 30-90 de minute, fără acces la datele tale interne.",
  alternates: {
    canonical: "/marketing-pentru-turism",
  },
  openGraph: {
    title:
      "Marketing pentru turism — audit digital gratuit | DeviDevs Agency",
    type: "website",
    url: `${siteUrl}/marketing-pentru-turism`,
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
      item: siteUrl,
    },
    {
      "@type": "ListItem",
      position: 2,
      name: "Marketing pentru turism",
      item: `${siteUrl}/marketing-pentru-turism`,
    },
  ],
};

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "De ce este auditul gratuit? Care e 'șmecheria'?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Nu există nicio 'șmecherie'. Auditul gratuit este modul nostru de a demonstra ce putem face. Vrem să vezi concret valoarea analizei noastre înainte de orice discuție despre colaborare. Nu ai nicio obligație după audit.",
      },
    },
    {
      "@type": "Question",
      name: "Ce se întâmplă, concret, după ce solicit auditul?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Completezi formularul (durează ~2 minute), iar noi analizăm automat prezența ta online folosind doar informații publice. În 30-90 de minute primești pe email un raport detaliat cu recomandări personalizate.",
      },
    },
    {
      "@type": "Question",
      name: "Sunt obligat(ă) să cumpăr ceva după audit?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Nu. Auditul și discuția de follow-up sunt 100% gratuite, fără nicio obligație. Dacă rezonezi cu recomandările noastre și vrei să mergem mai departe, discutăm opțiunile.",
      },
    },
    {
      "@type": "Question",
      name: "Aveți nevoie de acces la conturile mele?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Nu. Nu cerem parole, acces la conturi sau date financiare. Tot procesul de audit se bazează pe informații publice disponibile online.",
      },
    },
    {
      "@type": "Question",
      name: "În cât timp pot vedea rezultate?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Raportul de audit ajunge pe email în 30-90 de minute. Dacă decizi să implementezi recomandările, primele îmbunătățiri ale vizibilității online se văd de obicei în 4-8 săptămâni.",
      },
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
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />
      <HeroSection />
      <SectionDivider />
      <AudienceSection />
      <SectionDivider />
      <ProcessSection />
      <SectionDivider />
      <WhyUsSection />
      <SectionDivider />
      <FaqSection />
      <SectionDivider />
      <FinalCtaSection />
    </>
  );
}
