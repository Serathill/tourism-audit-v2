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
      name: "De ce este auditul gratuit? Care e smecheria?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Nu exista nicio smecherie. Auditul gratuit este modul nostru de a demonstra ce putem face. Vrem sa vezi concret valoarea analizei noastre inainte de orice discutie despre colaborare. Nu ai nicio obligatie dupa audit.",
      },
    },
    {
      "@type": "Question",
      name: "Ce se intampla, concret, dupa ce solicit auditul?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Completezi formularul (dureaza ~2 minute), iar noi analizam automat prezenta ta online folosind doar informatii publice. In 30-90 de minute primesti pe email un raport detaliat cu recomandari personalizate. Dupa aceea, daca doresti, programam o discutie gratuita de follow-up.",
      },
    },
    {
      "@type": "Question",
      name: "Sunt obligat(a) sa cumpar ceva dupa audit?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Nu. Auditul si discutia de follow-up sunt 100% gratuite, fara nicio obligatie. Daca rezonezi cu recomandarile noastre si vrei sa mergem mai departe, discutam optiunile. Daca nu, pastrezi raportul si il folosesti cum doresti.",
      },
    },
    {
      "@type": "Question",
      name: "Acest serviciu este pentru mine daca nu am o echipa de marketing?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Da, exact pentru tine este. Majoritatea proprietarilor de pensiuni si case de vacanta nu au o echipa dedicata de marketing. Auditul iti arata clar ce poti imbunatati, iar daca decizi sa colaboram, noi preluam totul.",
      },
    },
    {
      "@type": "Question",
      name: "Aveti nevoie de acces la conturile mele?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Nu. Nu cerem parole, acces la conturi sau date financiare. Tot procesul de audit se bazeaza pe informatii publice disponibile online. Este complet sigur si transparent.",
      },
    },
    {
      "@type": "Question",
      name: "In cat timp pot vedea rezultate?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Raportul de audit ajunge pe email in 30-90 de minute. Daca decizi sa implementezi recomandarile (singur sau cu noi), primele imbunatatiri ale vizibilitatii online se vad de obicei in 4-8 saptamani.",
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
